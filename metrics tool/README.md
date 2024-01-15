# CK
Code metrics for Java code by means of static analysis

## ck-master.zip #
Unmodified version of [ck-0.7.0](https://github.com/mauricioaniche/ck/releases/tag/ck-0.7.0).

## ck-modified.zip #
The modified version of [ck-0.7.0](https://github.com/mauricioaniche/ck/releases/tag/ck-0.7.0), which adds a try-catch statement to avoid program interruption caused by error reporting.

Unzip *ck-modified.zip*, and you can find the try-catch statement below in [here](ck-modified/src/main/java/com/github/mauricioaniche/ck/CK.java#Line109).

```
try{
	parser.createASTs(partition.toArray(new String[partition.size()]), null, new String[0], storage, null);
}catch (Exception e){

}
```
## ck.jar
We construct [ck.jar](ck.jar) based on the modified version.

## Environment

Windows 10 Professional Edition

Download amazon-corretto-11.0.18.10.1-windows-x64-jdk.zip from [here](https://corretto.aws/downloads/resources/11.0.18.10.1/amazon-corretto-11.0.18.10.1-windows-x64-jdk.zip).

Unzip amazon-corretto-11.0.18.10.1-windows-x64-jdk.zip to [jdk11](jdk11) in this directory.

## usage ##
`java -jar ck.jar <project dir> <use jars:true|false> <max files per partition, 0=automatic selection> <variables and fields metrics? True|False> <output dir> [ignored directories...]`

**e.g.,**   
`java -jar ck.jar C:\Users\xxx\Downloads\redisson-3.18.1 True 0 True C:\Users\xxx\Desktop\redisson-3.18.1` 


# Steps
1. Run [blockMetrics.py](blockMetrics.py) to calculate block-level metrics, and results can be found in [/metrics](/metrics).
2. Run [classAndMethodMetrics.py](classAndMethodMetrics.py) to calculate class-level and method-level metrics, and results can be found in [/metrics](/metrics).
3. Run [removePath.py](removePath.py) to remove the useless path and rename the column `file` as `FilePath`. 
4. Run [fileMetrics.py](fileMetrics.py) to calculate file-level metrics, and results can be found in [/metrics](/metrics).
