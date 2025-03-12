
# Test video dir.
"/storage/ywb/dataset/DL3DV_videos/DL3DV_points_50/1K/0a1b7c20a92c43c6b8954b1ac909fb2f0fa8b2997b80604bc8bbec80a1cb2da3/gt_0.mp4"

# step1: upsampling
## save in "/storage/ywb/dataset/event_results"
device=cuda:0
python upsampling/upsample.py --input_dir=example/original --output_dir=example/upsampled --device=$device

# step2: generate event stream
python esim_torch/generate_events.py --input_dir=example/upsampled \
                                     --output_dir=example/events \
                                     --contrast_threshold_neg=0.1 \
                                     --contrast_threshold_pos=0.1 \
                                     --refractory_period_ns=0


# task1: large scale video dataset
# task2: different threshold event stream