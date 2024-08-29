package com.baidu.ai.speech.realtime.nle.bean;

public interface NleCallback<T> {
    public void access(T result,String msg);
}
