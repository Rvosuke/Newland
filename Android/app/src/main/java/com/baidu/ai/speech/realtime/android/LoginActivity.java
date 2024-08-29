package com.baidu.ai.speech.realtime.android;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.baidu.ai.speech.realtime.R;
import com.baidu.ai.speech.realtime.nle.NleManager;

public class LoginActivity extends AppCompatActivity {

    private EditText usernameEdt;
    private EditText passwordEdt;

    private NleManager nleManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        nleManager = new NleManager();

        usernameEdt = findViewById(R.id.usernameEdt);
        passwordEdt = findViewById(R.id.passwordEdt);
        Button loginBtn = findViewById(R.id.loginBtn);
        loginBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                login();
            }
        });
    }

    public void login() {
        String account = usernameEdt.getText().toString();
        String password = passwordEdt.getText().toString();

        nleManager.doLogin(account, password, (isOK, errMsg) -> {
            if (isOK) {
                // 当登录成功后，跳转到主页
                startActivity(new Intent(this, MainActivity.class));
            } else {
                Toast.makeText(this, errMsg, Toast.LENGTH_SHORT).show();
            }
        });

        boolean isOk = false;
        String errMsg = "";
    }

}
