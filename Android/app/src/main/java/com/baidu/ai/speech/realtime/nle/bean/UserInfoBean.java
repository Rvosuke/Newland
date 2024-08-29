package com.baidu.ai.speech.realtime.nle.bean;

public class UserInfoBean {
    private Integer UserID;
    private String UserName;
    private String Email;
    private String Telphone;
    private Boolean Gender;
    private Integer CollegeID;
    private String CollegeName;
    private String RoleName;
    private Integer RoleID;
    private String AccessToken;
    private Integer AccessTokenErrCode;
    private String ReturnUrl;
    private String DataToken;

    public Integer getUserID() {
        return UserID;
    }
    public void setUserID(Integer userID) {
        UserID = userID;
    }
    public String getUserName() {
        return UserName;
    }
    public void setUserName(String userName) {
        UserName = userName;
    }
    public String getEmail() {
        return Email;
    }

    public void setEmail(String email) {
        Email = email;
    }

    public String getTelphone() {
        return Telphone;
    }

    public void setTelphone(String telphone) {
        Telphone = telphone;
    }

    public Boolean getGender() {
        return Gender;
    }

    public void setGender(Boolean gender) {
        Gender = gender;
    }

    public Integer getCollegeID() {
        return CollegeID;
    }

    public void setCollegeID(Integer collegeID) {
        CollegeID = collegeID;
    }

    public String getCollegeName() {
        return CollegeName;
    }

    public void setCollegeName(String collegeName) {
        CollegeName = collegeName;
    }

    public String getRoleName() {
        return RoleName;
    }

    public void setRoleName(String roleName) {
        RoleName = roleName;
    }

    public Integer getRoleID() {
        return RoleID;
    }

    public void setRoleID(Integer roleID) {
        RoleID = roleID;
    }

    public String getAccessToken() {
        return AccessToken;
    }

    public void setAccessToken(String accessToken) {
        AccessToken = accessToken;
    }

    public Integer getAccessTokenErrCode() {
        return AccessTokenErrCode;
    }

    public void setAccessTokenErrCode(Integer accessTokenErrCode) {
        AccessTokenErrCode = accessTokenErrCode;
    }

    public String getReturnUrl() {
        return ReturnUrl;
    }

    public void setReturnUrl(String returnUrl) {
        ReturnUrl = returnUrl;
    }

    public String getDataToken() {
        return DataToken;
    }

    public void setDataToken(String dataToken) {
        DataToken = dataToken;
    }
}
