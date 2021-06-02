package com.ccn.ncodeview.application;

import android.app.Dialog;
import android.content.Context;
import android.os.Bundle;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.view.WindowManager;
import android.widget.ImageView;
import android.widget.SeekBar;
import android.widget.SeekBar.OnSeekBarChangeListener;
import com.ccn.ncodeview.R;

import androidx.annotation.NonNull;

/**
 * 亮度和对比度弹出框
 */
public class SettingDialog extends Dialog implements android.view.View.OnClickListener, OnSeekBarChangeListener {
    private SeekBar mLightSeekBar;
    private SeekBar mContrastSeekBar;
    private ImageView mIvBack;
    private Context context;
    private View customView;
    private LeaveDialogListener listener;
    private int lightValue = 0;
    private int contrastValue = 0;

    @Override
    public void onProgressChanged(SeekBar seekBar, int i, boolean b) {
        mListener.onChange(seekBar, i, b);
    }

    @Override
    public void onStartTrackingTouch(SeekBar seekBar) {

    }

    @Override
    public void onStopTrackingTouch(SeekBar seekBar) {

    }
    private SeekBarChangedListener mListener;//监听SeekBar事件，比如拖动等
    /*获取监听对象*/
    public SeekBarChangedListener getmListener() {
        return mListener;
    }
    /*设置监听对象*/
    public void setmListener(SeekBarChangedListener mListener) {
        this.mListener = mListener;
    }


    public interface SeekBarChangedListener{
        public void onChange(SeekBar seekBar, int progress, boolean fromUser);
    }

    public interface LeaveDialogListener{
        public void onClick(View view);
    }

    @Override
    public void onClick(View v) {
        // TODO Auto-generated method stub
        listener.onClick(v);
    }


    public SettingDialog(@NonNull Context context) {
        super(context, R.style.BottomDialog);
    }

    public SettingDialog(@NonNull Context context, int theme, LeaveDialogListener listener, SeekBarChangedListener mListener, int lightValue, int contrastValue) {
        super(context, theme);
        this.context = context;
        LayoutInflater inflater = LayoutInflater.from(context);
        customView = inflater.inflate(R.layout.set_light_layout, (ViewGroup) findViewById(R.id.setting_dialog_ll));
        this.listener = listener;
        this.mListener = mListener;
        this.lightValue = lightValue;
        this.contrastValue = contrastValue;
    }
    public View getCustomView() {
        return customView;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.set_light_layout);
        mLightSeekBar = findViewById(R.id.sb_light);
        mContrastSeekBar = findViewById(R.id.sb_contrast);
        mIvBack = findViewById(R.id.iv_back);
        Window window = this.getWindow();
        WindowManager.LayoutParams lp = window.getAttributes();
        lp.width = getContext().getResources().getDisplayMetrics().widthPixels;
        window.setGravity(Gravity.BOTTOM);
        window.setAttributes(lp);
        setCanceledOnTouchOutside(true);
        setCancelable(true);
        mLightSeekBar.setOnSeekBarChangeListener(this);
        mContrastSeekBar.setOnSeekBarChangeListener(this);
        mIvBack.setOnClickListener(this);
//        mLightSeekBar.setProgress(lightValue);
//        mContrastSeekBar.setProgress(contrastValue);
    }
}