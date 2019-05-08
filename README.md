* pytorch-explanatory-commentary-element-recognition
* it is similar to a sequence labeling task, you can regard as NER task. In my project, we use eval standard is same as conll2003 dataset 
* enviroment: pytorch 0.4.1, python 3.6.1, cuda 8.0 or cuda 9.0
* method:
  * bilstm + crf as based framework
  * bilstm + cnn + crf, add strokes features by cnn
* data:
  * hotel & phone domain commentary sentences, show three small dataset in Data file
* Usage
 * modify the config file, detail see the Config directory <br
	  * Train:
		    * the training process is aim at saving the best nn moudle
      * GPU: setting GPU process and run "python -u main.py ", or you could wirte script
      * cpu: run main.py file
	  * Test:
	   	* Decoding test data, and write decode result to file.
		   * (1) you should change function parse_argument() of main.py file, setting "dest=test" as "True", default = "False" for training
		   * (2) run "python -u main.py" in your GPU or main.py file
	  * Eval:
		   * For the decode result file, use conlleval script in Tools directory to calculate F-score.
* result: 
  * hotel  
  * phone
* this project some codes refer to my classmate, https://github.com/bamtercelboo/pytorch_NER_BiLSTM_CNN_CRF.  if you had any question, you'd sent email to him or me for this project. his address is bamtercelboo@gmail.com or bamtercelboo@163.com and my address is fzh_common@163.com .
