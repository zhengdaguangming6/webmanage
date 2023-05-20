APP_ENV = {
    "yapi": {
        "qa_domain": "http://yapi.{id}.haohaoce.com",
        "gray_domain": "http://yapi.{id}.haohaozhu.me",
        "online_domain": "https://yapi.haohaozhu.cn",
    },
    "tapi": {
        "qa_domain": "http://tapi.{id}.haohaoce.com",
        "gray_domain": "http://tapi.{id}.haohaozhu.me",
        "online_domain": "https://tapi.haohaozhu.cn",
    },
    "m": {
        "qa_domain": "http://m.{id}.haohaoce.com",
        "gray_domain": "http://m.{id}.haohaozhu.me",
        "online_domain": "https://m.haohaozhu.cn",
    },
}

BACKSTAGE_ENV = {
    "dapi": {
        "qa_domain": "http://dapi.{id}.haohaoce.com",
        "gray_domain": "http://dapi.{id}.haohaozhu.me",
        "online_domain": "https://dapi.haohaozhu.cn",
    }
}


METHOD_PARAMS = {
    "GET": "params",
    "POST": {
        "data": "data",
        "json": "json"
    }

}

