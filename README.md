# 说明
> 此项目用于建立情感分析模型，主要想法是，通过收集特定的评论数据，标注评价是好的还是坏的  
> 可以重新修改标注结果, 然后通过通过训练生成检测模型后，可以用于新的评论的情绪预测  

# 使用说明
[前端代码库](https://github.com/bxxfighting/emotion-web)

安装环境：  
python 3.6.8  
```
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```
执行命令:  
```
python manage.py migrate
python manage.py makemigrations account dataset
python manage.py migrate
python manage.py create_super_user root root
python manage.py init_dataset
python manage.py train
```

# 前端说明
> 如果想要修正评论数据或者停止词，可以clone前端代码编译后，使用  

# 注意
1. 有关stopwords
对于stopwords其实不同场景，需求是不同的，我开始拿到这个stopwords文件时，直接使用的,  
但是其实不应该这样，而是要根据你实际使用场景来进行增加删.  
比如在stopwords里有“一般”这个词，但是这里练习使用的是外卖的评价，  
一般是经常会出现的，而且会是负面评价中的一个重要点, 所以不能当作stopwords  

# 借鉴内容如下：
* 主要参考: https://www.jianshu.com/p/29aa3ad63f9d  
* stopwords来源：https://github.com/chdd/weibo/tree/master/stopwords
* 外卖评价来源：https://github.com/SophonPlus/ChineseNlpCorpus
