---
license: other
base_model: google/mobilenet_v2_1.0_224
tags:
- generated_from_trainer
datasets:
- food101
metrics:
- accuracy
model-index:
- name: mobilenet-finetuned-food101
  results:
  - task:
      name: Image Classification
      type: image-classification
    dataset:
      name: food101
      type: food101
      config: default
      split: train[:5000]
      args: default
    metrics:
    - name: Accuracy
      type: accuracy
      value: 0.821
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# mobilenet-finetuned-food101

This model is a fine-tuned version of [google/mobilenet_v2_1.0_224](https://huggingface.co/google/mobilenet_v2_1.0_224) on the food101 dataset.
It achieves the following results on the evaluation set:
- Loss: 0.5518
- Accuracy: 0.821

## Model description

More information needed

## Intended uses & limitations

More information needed

## Training and evaluation data

More information needed

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 5e-05
- train_batch_size: 128
- eval_batch_size: 128
- seed: 42
- gradient_accumulation_steps: 4
- total_train_batch_size: 512
- optimizer: Adam with betas=(0.9,0.999) and epsilon=1e-08
- lr_scheduler_type: linear
- lr_scheduler_warmup_ratio: 0.1
- num_epochs: 30

### Training results

| Training Loss | Epoch | Step | Validation Loss | Accuracy |
|:-------------:|:-----:|:----:|:---------------:|:--------:|
| No log        | 1.0   | 6    | 1.9575          | 0.153    |
| 1.9536        | 2.0   | 12   | 1.8509          | 0.265    |
| 1.9536        | 3.0   | 18   | 1.7003          | 0.451    |
| 1.7915        | 4.0   | 24   | 1.5181          | 0.578    |
| 1.4994        | 5.0   | 30   | 1.3609          | 0.631    |
| 1.4994        | 6.0   | 36   | 1.2321          | 0.669    |
| 1.2203        | 7.0   | 42   | 1.0696          | 0.69     |
| 1.2203        | 8.0   | 48   | 0.9676          | 0.723    |
| 1.0215        | 9.0   | 54   | 0.8888          | 0.729    |
| 0.8462        | 10.0  | 60   | 0.8380          | 0.74     |
| 0.8462        | 11.0  | 66   | 0.7461          | 0.778    |
| 0.744         | 12.0  | 72   | 0.6724          | 0.792    |
| 0.744         | 13.0  | 78   | 0.7314          | 0.769    |
| 0.6496        | 14.0  | 84   | 0.6831          | 0.77     |
| 0.6143        | 15.0  | 90   | 0.5937          | 0.81     |
| 0.6143        | 16.0  | 96   | 0.6217          | 0.793    |
| 0.5468        | 17.0  | 102  | 0.5965          | 0.788    |
| 0.5468        | 18.0  | 108  | 0.5944          | 0.813    |
| 0.5428        | 19.0  | 114  | 0.5869          | 0.812    |
| 0.5193        | 20.0  | 120  | 0.5565          | 0.82     |
| 0.5193        | 21.0  | 126  | 0.6155          | 0.803    |
| 0.4902        | 22.0  | 132  | 0.5685          | 0.817    |
| 0.4902        | 23.0  | 138  | 0.6097          | 0.789    |
| 0.4869        | 24.0  | 144  | 0.6002          | 0.8      |
| 0.4745        | 25.0  | 150  | 0.5569          | 0.814    |
| 0.4745        | 26.0  | 156  | 0.5414          | 0.821    |
| 0.4653        | 27.0  | 162  | 0.5806          | 0.807    |
| 0.4653        | 28.0  | 168  | 0.5663          | 0.807    |
| 0.4543        | 29.0  | 174  | 0.5412          | 0.825    |
| 0.4575        | 30.0  | 180  | 0.5518          | 0.821    |


### Framework versions

- Transformers 4.35.2
- Pytorch 2.1.0+cu118
- Datasets 2.15.0
- Tokenizers 0.15.0
