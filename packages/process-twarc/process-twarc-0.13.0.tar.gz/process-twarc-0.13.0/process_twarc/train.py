
from transformers import Trainer, AutoTokenizer, AutoModelForMaskedLM, TrainingArguments, DataCollatorForLanguageModeling, TrainerCallback, EarlyStoppingCallback, get_polynomial_decay_schedule_with_warmup
from torch.optim import AdamW
from torch.utils.data import DataLoader
from process_twarc.util import  load_dict, load_tokenizer, load_model
from process_twarc.preprocess import generate_splits
import torch
import wandb
import optuna
import os

def MLM_sweep(
    data_dir: str,
    path_to_tokenizer: str,
    path_to_model: str,
    checkpoint_dir: str,
    path_to_search_space: str,
    path_to_storage: str,
    n_trials: int=1,
    enable_pruning: bool=False,
    evaluation_strategy: str="steps",
    eval_steps: float=float(1/12),
    save_strategy: str="steps",
    save_steps: float=float(1/12),
    save_total_limit: int=3,
    metric_for_best_model: str="eval_loss",
    push_to_hub: bool=False,
    patience: int=3,
    print_details: bool=True,
    report_to: str="wandb"
):

    def objective(trial):

        def init_trial(checkpoint_dir):
            """Initialize a new trial directory for saving checkpoints."""

            def get_next_trial(last_trial):
                """Get the next trial name based on the last trial name."""
                numeric_part = int(last_trial[5:])
                numeric_part += 1
                next_trial = "trial" + str(numeric_part).zfill(3)
                return next_trial
            
            trials = os.listdir(checkpoint_dir)
            if trials == []:
                next_trial = "trial001"
            else:
                last_trial = sorted(trials, reverse=True)[0]
                next_trial = get_next_trial(last_trial)
            
            trial_dir = f"{checkpoint_dir}/{next_trial}"
            os.mkdir(f"{trial_dir}")
            print(f"Generated folder for {next_trial}")
            return trial_dir
        
        def init_hyperparameters(trial, path_to_search_space):
            """Initialize hyperparameters for the trial."""

            search_space = load_dict(path_to_search_space)
            project = search_space["project"]
            group = search_space["group"]

            #Regularizers
            hidden_dropout_prob=trial.suggest_float(
                "hidden_dropout_prob", 
                search_space["hidden_dropout_prob"]["low"], 
                search_space["hidden_dropout_prob"]["high"],
                step=search_space["hidden_dropout_prob"]["step"],
                log=search_space["hidden_dropout_prob"]["log"])
            
            attention_dropout_prob=trial.suggest_float(
                "attention_dropout_prob", 
                search_space["attention_dropout_prob"]["low"], 
                search_space["attention_dropout_prob"]["high"], 
                step=search_space["attention_dropout_prob"]["step"],
                log=search_space["attention_dropout_prob"]["log"])
            
            weight_decay=trial.suggest_float(
                "weight_decay",
                search_space["weight_decay"]["low"], 
                search_space["weight_decay"]["high"], 
                step=search_space["weight_decay"]["step"],
                log=search_space["weight_decay"]["log"])

            #Shape the learning rate
            num_train_epochs = trial.suggest_int(
                "num_train_epochs", 
                search_space["num_train_epochs"]["low"],
                search_space["num_train_epochs"]["high"],
                step=search_space["num_train_epochs"]["step"],
                log=search_space["num_train_epochs"]["log"]) 
            
            initial_learning_rate = trial.suggest_float(
                "initial_learning_rate",
                search_space["initial_learning_rate"]["low"],
                search_space["initial_learning_rate"]["high"],
                step=search_space["initial_learning_rate"]["step"],
                log=search_space["initial_learning_rate"]["log"])
            
            num_warmup_steps = trial.suggest_int(
                "num_warmup_steps",
                search_space["num_warmup_steps"]["low"],
                search_space["num_warmup_steps"]["high"],
                step=search_space["num_warmup_steps"]["step"],
                log=search_space["num_warmup_steps"]["log"])
            
            power = trial.suggest_float(
                "power",
                search_space["power"]["low"],
                search_space["power"]["high"],
                step=search_space["power"]["step"],
                log=search_space["power"]["log"])

            #Optimizer
            adam_beta1 = trial.suggest_float(
                "adam_beta1",
                search_space["adam_beta1"]["low"],
                search_space["adam_beta1"]["high"],
                step=search_space["adam_beta1"]["step"],
                log=search_space["adam_beta1"]["log"])
            
            adam_beta2 = trial.suggest_float(
                "adam_beta2",
                search_space["adam_beta2"]["low"],
                search_space["adam_beta2"]["high"],
                step=search_space["adam_beta2"]["step"],
                log=search_space["adam_beta2"]["log"])
                 
            adam_epsilon = trial.suggest_float(
                "adam_epsilon",
                search_space["adam_epsilon"]["low"],
                search_space["adam_epsilon"]["high"],
                step=search_space["adam_epsilon"]["step"],
                log=search_space["adam_epsilon"]["log"])

            fixed_params = {
                "per_device_train_batch_size": 55,
                "per_device_eval_batch_size": 75
            }

            variable_params = {
                "hidden_dropout_prob": hidden_dropout_prob,
                "attention_dropout_prob": attention_dropout_prob,
                "weight_decay": weight_decay,
                "num_train_epochs": num_train_epochs,
                "initial_learning_rate": initial_learning_rate,
                "num_warmup_steps": num_warmup_steps,
                "power": power,
                "adam_beta1": adam_beta1,
                "adam_beta2": adam_beta2,
                "adam_epsilon": adam_epsilon
            }

            wandb.init(
                project=project,
                group=group,  
                entity="lonewolfgang",
                config ={
                "meta": {
                    "_name_or_path": "LoneWolfgang/bert-for-japanese-twitter"},
                "model":{
                    "model_type": "bert",
                    "hidden_act": "gelu",
                    "hidden_size": 768,
                    "num_hidden_layers": 12,
                    "intermediate_size": 3072,
                    "num_attention_heads": 12,
                    "max_position_embeddings": 512,
                    "position_embedding_type": "absolute",
                    "vocab_size": 32_003,
                    "initializer_range": 0.02,
                    "attention_dropout_prob": attention_dropout_prob,
                    "hidden_dropout_prob": hidden_dropout_prob,
                    "weight_decay": weight_decay,
                    "layer_norm_eps": 1e-12,
                },
                "optimizer":{
                    "optim": "adamw_hf",
                    "lr_scheduler_type": "polynomial",
                    "initial_learning_rate": initial_learning_rate,
                    "final_learning_rate": 0.0,
                    "power": power,
                    "num_warmup_steps": num_warmup_steps,
                    "adam_beta1": adam_beta1,
                    "adam_beta2": adam_beta2,
                    "adam_epsilon": adam_epsilon,
                },
                "trainer": {
                    "num_train_epochs": num_train_epochs,
                    "logging_strategy": "steps",
                    "logging_steps": 500,
                    "per_device_eval_batch_size": 75,
                    "per_device_train_batch_size": 55,
                    "eval_strategy": "steps",
                    "eval_steps": 31_912,
                    "save_strategy": "steps",
                    "save_steps": 31_912,
                    "patience": 3,
                    "save_total_limit": 3,
                    "metric_for_best_model": "eval_loss",
                    "seed": 42
                }
            })
        
            print("\nVariable Params:")
            for key in variable_params:
                print(key, variable_params[key])
            print("\nFixed Params:")
            for key in fixed_params:
                print(key, fixed_params[key])
            
            return variable_params, fixed_params

        def collate_data(collator_class, tokenizer, tokenized_dataset, per_device_train_batch_size, print_details=print_details):
            data_collator = collator_class(tokenizer)
            train_dataloader = DataLoader(
                tokenized_dataset,
                batch_size=per_device_train_batch_size,
                shuffle=True,
                collate_fn=data_collator
            )
            if print_details:
                print("Data collated.")
                print(f"\nBatch Size: {per_device_train_batch_size}")
                print("Shape of first five batches:")
                for step, batch in enumerate(train_dataloader):
                    print(batch["input_ids"].shape)
                    if step > 5:
                        break
            return data_collator


        splits = generate_splits(data_dir)
        train_dataset = splits["train"]
        eval_dataset = splits["validation"]
        test_dataset = splits["development"]

        trial_dir=init_trial(checkpoint_dir)
        variable_params, fixed_params = init_hyperparameters(trial, path_to_search_space)
        per_device_train_batch_size, per_device_eval_batch_size = fixed_params.values()
        hidden_dropout_prob, attention_dropout_prob, weight_decay, num_train_epochs, initial_learning_rate, num_warmup_steps, power, adam_beta1, adam_beta2, adam_epsilon = variable_params.values()

        device = "cuda" if torch.cuda.is_available() else RuntimeError("No GPU available.")

        tokenizer = load_tokenizer(path_to_tokenizer, AutoTokenizer, print_details=print_details)
        model = load_model(path_to_model, AutoModelForMaskedLM, device=device, print_details=print_details)
        model.config.hidden_dropout_prob = hidden_dropout_prob
        model.config.attention_dropout_prob = attention_dropout_prob

        data_collator = collate_data(DataCollatorForLanguageModeling, tokenizer, train_dataset, per_device_train_batch_size)

        optimizer = AdamW(
            params=model.parameters(),
            lr=initial_learning_rate,
            betas = (adam_beta1, adam_beta2),
            eps=adam_epsilon,
            weight_decay=weight_decay)
        
        scheduler = get_polynomial_decay_schedule_with_warmup(
            optimizer=optimizer,
            num_warmup_steps=num_warmup_steps,
            num_training_steps=len(train_dataset)//per_device_train_batch_size * num_train_epochs,
            lr_end=0.0,
            power=power
        )

        training_args = TrainingArguments(
            output_dir=trial_dir,
            evaluation_strategy=evaluation_strategy,
            eval_steps=eval_steps/num_train_epochs,
            num_train_epochs=num_train_epochs,
            save_strategy=save_strategy,
            save_steps=save_steps/num_train_epochs,
            save_total_limit=save_total_limit,
            push_to_hub=push_to_hub,
            per_device_train_batch_size=per_device_train_batch_size,
            per_device_eval_batch_size=per_device_eval_batch_size,
            load_best_model_at_end=True, 
            metric_for_best_model=metric_for_best_model,
            report_to=report_to
        )

        class OptunaCallback(TrainerCallback):
            def __init__(self, trial, should_prune=True):
                self.trial = trial
                self.should_prune = should_prune

            def on_evaluate(self, args, state, control, metrics=None, **kwargs):
                eval_loss = metrics.get("eval_loss")
                self.trial.report(eval_loss, step=state.global_step)
                if self.should_prune and self.trial.should_prune():
                    raise optuna.TrialPruned()

        trainer = Trainer(
            model=model,
            args=training_args,
            data_collator=data_collator,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            tokenizer=tokenizer,
            optimizers=(optimizer, scheduler),
            callbacks=[EarlyStoppingCallback(early_stopping_patience=patience),
                       OptunaCallback(trial, should_prune=enable_pruning)]
        )
        trainer.train()
        results = trainer.evaluate(test_dataset)
        print("\nResults:", results)
        wandb.log(results)
        trainer.save_model()

        return results["eval_loss"]
        
    study = optuna.create_study(
        direction="minimize",
        study_name="bert-for-japanese-twitter",
        load_if_exists=True,
        storage=path_to_storage)
    study.optimize(objective, n_trials=n_trials)
