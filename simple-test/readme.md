# Shell scripts to do simple test

## Recommend to use this very very simple script, if the condition/testcase is allowed.

``` bash
#!/usr/bin/bash
emon_dir=/home/jinjun/tools/emon-scripts

timets=$(date "+%Y%m%d%H%M")
name="resnet50_tf_1.14.0_${timets}"
echo "=================== ${name} ==================="

data=$(pwd)/data
mkdir -p $data


# start emon
bash ${emon_dir}/run_emon.sh $name


python tf_cnn_benchmarks.py --device=cpu --nodistortions --mkl=True --forward_only=True -data_format=NHWC --model=resnet50 --n
um_inter_threads=2 --num_intra_threads=48 -batch_size=128 | tee -a result.log


# stop emon
bash ${emon_dir}/stop_emon.sh
mv *.log ${emon_dir}/${name}
mv ${emon_dir}/${name} ${data}
```

## For a little complex testcase, please see ``runme.sh``.
