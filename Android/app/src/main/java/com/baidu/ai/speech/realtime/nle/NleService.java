package com.baidu.ai.speech.realtime.nle;

import com.baidu.ai.speech.realtime.nle.bean.BaseBean;
import com.baidu.ai.speech.realtime.nle.bean.UserBean;
import com.baidu.ai.speech.realtime.nle.bean.UserInfoBean;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.POST;

public interface NleService {
    public static final String BASE_URL = "http://api.nlecloud.com/";

    @POST("Users/Login")
    public Call<BaseBean<UserInfoBean>> doLogin(@Body UserBean user);
}