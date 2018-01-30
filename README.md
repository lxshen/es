# es
elasticsearch分词

nishi

Bool 组合查询
Filter  过滤
Must  如果有多个条件，这些条件必须都满足
Should 如果有多个条件，满足一个或多个即可
Must_not 和must相反

过滤出工资是15000 的
```
GET 51jobs/job/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match_all": {}
        }
      ],
      "filter": {
        "term": {
          "salary": 15000
        }
      }
    }
  }
}
```

检索出“salary”是12000或者“title”是“监控”的并且“salary”不能是8000和“10000”
```
GET 51jobs/job/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "term": {
            "salary": {
              "value": "12000"
            }
          }
        },
        {
          "term": {
            "title": {
              "value": "监控"
            }
          }
        }
      ],
      "must_not": [
        {
          "term": {
            "salary": {
              "value": "10000"
            }
          }
        },
        {
          "term": {
            "salary": {
              "value": "8000"
            }
          }
        }
      ]
    }
  }
}
```

过滤空值
检索出工资不为空的

```
GET 51jobs/job/_search
{
  "query": {
    "bool": {
      "filter": {
        "exists": {
          "field": "salary"
        }
      }
    }
  }
}
```

检索出城市为空的

```
GET 51jobs/job/_search
{
  "query": {
    "bool": {
      "must_not": [
        {
          "exists":{
            "field": "city" 
          }
        }
      ]
    }
  }
}
```


