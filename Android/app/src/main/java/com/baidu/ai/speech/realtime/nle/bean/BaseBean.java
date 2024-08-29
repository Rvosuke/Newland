package com.baidu.ai.speech.realtime.nle.bean;

import java.io.Serializable;

public class BaseBean<T> implements Serializable {

    private T ResultObj;
    private int Status;
    private int StatusCode;
    private String Msg;
    private Object ErrorObj;

    public Object getErrorObj() {
        return ErrorObj;
    }
    public void setErrorObj(Object errorObj) {
        ErrorObj = errorObj;
    }
    public void setMsg(String msg) {
        Msg = msg;
    }
    public void setErrorObj(String errorObj) {
        ErrorObj = errorObj;
    }
    public void setStatus(int status) {
        Status = status;
    }
    public void setStatusCode(int statusCode) {
        StatusCode = statusCode;
    }
    public void setResultObj(T resultObj) {
        ResultObj = resultObj;
    }
    public int getStatus() {
        return Status;
    }
    public int getStatusCode() {
        return StatusCode;
    }
    public String getMsg() {
        return Msg;
    }
    public T getResultObj() {
        return ResultObj;
    }
}
