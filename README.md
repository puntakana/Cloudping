# Cloudping

Cloudping is a command line tools that reports latency to differents clouder (AWS, Azure, GCP). 

```
usage: Get Latency from list of dict [-h] [-o OUTPUT]
                                     [--cloud {gcp,aws,azure}]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Format of the output
  --cloud {gcp,aws,azure}
                        Clouder, can take value "gcp" / "aws" "azure"
```

```
python3.7 cloudping.py --cloud aws
              Name              IP  Latency in ms
1        eu-west-3    52.95.155.53         18.779
2        eu-west-2    52.95.150.48         24.531
3     eu-central-1   52.219.72.155         28.087
4        eu-west-1    52.218.41.35         32.820
5       eu-north-1    52.95.170.21         41.901
6     ca-central-1   52.95.147.180        109.786
7        us-east-2   52.219.80.170        123.807
8       ap-south-1   52.219.66.105        136.205
9        us-west-1    52.219.113.8        154.301
10       us-west-2  52.218.220.144        170.781
11  ap-southeast-1  52.219.132.158        190.653
12       sa-east-1    52.95.164.34        214.756
13  ap-northeast-1   52.219.136.10        255.982
14  ap-northeast-2   52.219.56.145        282.950
15  ap-southeast-2   52.95.134.239        296.045
```