package com.baidu.ai.speech.realtime.nle;

import androidx.annotation.NonNull;

import com.baidu.ai.speech.realtime.nle.bean.BaseBean;
import com.baidu.ai.speech.realtime.nle.bean.NleCallback;
import com.baidu.ai.speech.realtime.nle.bean.UserBean;
import com.baidu.ai.speech.realtime.nle.bean.UserInfoBean;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Converter;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.adapter.rxjava3.RxJava3CallAdapterFactory;
import retrofit2.converter.gson.GsonConverterFactory;

public class NleManager {
    private final NleService nleService;
    private String token;

    public NleManager(){
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl(NleService.BASE_URL)
                .addConverterFactory(GsonConverterFactory.create())
                .addCallAdapterFactory(RxJava3CallAdapterFactory.create())
                .build();

        nleService = retrofit.create(NleService.class);
        // nleService 是 retrofit 构建的一个接口对象，可以使用库中的大部分方法了
    }

    public void doLogin(String account, String password, NleCallback<Boolean> nleCallback){
        UserBean user = new UserBean(account, password);
        Call<BaseBean<UserInfoBean>> call = nleService.doLogin(user);
        call.enqueue(new Callback<BaseBean<UserInfoBean>>() {
            // enqueue 方法是用于在后台（异步）执行网络请求的。
            // 与同步请求不同，异步请求不会阻塞主线程（通常是UI线程），因此可以避免在请求进行时应用程序界面卡住。


            // 以下是两个回调方法， 当请求成功并且服务器返回了一个响应时，onResponse 方法会被调用。
            // 这里可以处理服务器的响应数据。
            @Override  // Override 是覆盖的显式声明。覆盖是类的继承中的一个模式。
            public void onResponse(@NonNull Call<BaseBean<UserInfoBean>> call,
                                   @NonNull Response<BaseBean<UserInfoBean>> response) {
                String errMsg = response.message();
                if (response.code() == 200){
                    BaseBean<UserInfoBean> respJson = response.body();
                    assert respJson != null;
                    errMsg = respJson.getMsg();
                    if(respJson.getStatus() == 0){
                        UserInfoBean userInfo = respJson.getResultObj();
                        token = userInfo.getAccessToken();

                        System.out.println(errMsg + "\n Token: " + token);
                        nleCallback.access(true, errMsg);
                        return;
                    }
                } else {
                    nleCallback.access(false, errMsg);
                }
            }

            // 一般是会得到响应的，而有时是因为网络问题或者服务器关闭，所以无法访问，此时会回调onFailure方法。
            @Override
            public void onFailure(@NonNull Call<BaseBean<UserInfoBean>> call,
                                  @NonNull Throwable t) {
                System.out.println("Network or Server Error: " + t.getMessage());
            }
        });
    }

    public void cmds(){
//        nleService.
    }
}
