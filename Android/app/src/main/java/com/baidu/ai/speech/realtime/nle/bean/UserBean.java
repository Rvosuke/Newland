package com.baidu.ai.speech.realtime.nle.bean;

public class UserBean {
    //    {
//        "Account": "18368519766",
//            "Password": "a78945612355b"
//    }
    private String Account;
    private String Password;

    public UserBean() {
    }

    public UserBean(String account, String password) {
        Account = account;
        Password = password;
    }

    public String getAccount() {
        return Account;
    }

    public void setAccount(String account) {
        Account = account;
    }

    public String getPassword() {
        return Password;
    }

    public void setPassword(String password) {
        Password = password;
    }
}