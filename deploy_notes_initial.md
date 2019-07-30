1. SSH into the machine (Amazon Linux EC2)
2. Execute the following commands:
  1. `sudo update yum`
  2. `sudo yum install git`
  3. `git clone https://github.com/codeforgreenville/upstate_tech_cal_service.git`
  4. `cd upstate_tech_cal_service`
  5. `curl https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -o miniconda.sh`
  6. `sh miniconda.sh -b -p $HOME/miniconda`
  7. `export PATH="$HOME/miniconda/bin:$PATH"`
  8. `conda env create -f environment.yml`
  9. `source activate cal_service`
3. Create a config file as shown in config.ini.example
