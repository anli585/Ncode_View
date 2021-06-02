package com.ccn.ncodeview.view;

import android.graphics.Bitmap;
import android.hardware.usb.UsbDevice;
import android.os.Bundle;
import android.os.Handler;

import android.text.TextUtils;
import android.util.Base64;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.Surface;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.Toast;
import com.ccn.ncodeview.R;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

import com.ccn.ncodeview.UVCCameraHelper;
import com.ccn.ncodeview.application.MyApplication;
import com.ccn.ncodeview.application.SettingDialog;
import com.ccn.ncodeview.utils.FileUtils;
import com.serenegiant.usb.CameraDialog;
import com.serenegiant.usb.Size;
import com.serenegiant.usb.USBMonitor;
import com.serenegiant.usb.common.AbstractUVCCameraHandler;
import com.serenegiant.usb.encoder.RecordParams;
import com.serenegiant.usb.widget.CameraViewInterface;

import java.io.ByteArrayOutputStream;
import java.util.ArrayList;
import java.util.List;

import butterknife.BindView;
import butterknife.ButterKnife;

import com.ccn.ncodeview.utils.PythonInit;

/**
 * UVCCamera use demo
 * <p>
 * Created by jiangdongguo on 2017/9/30.
 */

public class USBCameraActivity extends AppCompatActivity implements CameraDialog.CameraDialogParent, CameraViewInterface.Callback {

    private static final String TAG = "Debug";
    @BindView(R.id.camera_view)
    public View mTextureView;
    @BindView(R.id.toolbar)
    public Toolbar mToolbar;

    public SettingDialog settingDialog = null;
    public SeekBar mSeekBrightness = null;
    public SeekBar mSeekContrast = null;
    public ImageView mIvBack = null;

    @BindView(R.id.tv_light)
    public TextView mTvLight;

    @BindView(R.id.tv_resolution)
    public TextView mTvResolution;

    @BindView(R.id.tv_camera)
    public TextView mTvCamera;

    private UVCCameraHelper mCameraHelper;
    private CameraViewInterface mUVCCameraView;
    private AlertDialog mDialog;

    private boolean isRequest;
    private boolean isPreview;

    private UVCCameraHelper.OnMyDevConnectListener listener = new UVCCameraHelper.OnMyDevConnectListener() {

        @Override
        public void onAttachDev(UsbDevice device) {
            // request open permission
            if (!isRequest) {
                isRequest = true;
                if (mCameraHelper != null) {
                    mCameraHelper.requestPermission(0);
                }
            }
        }

        @Override
        public void onDettachDev(UsbDevice device) {
            // close camera
            if (isRequest) {
                isRequest = false;
                mCameraHelper.closeCamera();
                showShortMsg(device.getDeviceName() + " is out");
            }
        }

        @Override
        public void onConnectDev(UsbDevice device, boolean isConnected) {
            if (!isConnected) {
                showShortMsg("fail to connect,please check resolution params");
                isPreview = false;
            } else {
                isPreview = true;
                showShortMsg("connecting");
                // initialize seekbar
                // need to wait UVCCamera initialize over
//                new Thread(new Runnable() {
//                    @Override
//                    public void run() {
//                        try {
//                            Thread.sleep(2500);
//                        } catch (InterruptedException e) {
//                            e.printStackTrace();
//                        }
//                        Looper.prepare();
////                        if(mCameraHelper != null && mCameraHelper.isCameraOpened()) {
////                            mSeekBrightness.setProgress(mCameraHelper.getModelValue(UVCCameraHelper.MODE_BRIGHTNESS));
////                            mSeekContrast.setProgress(mCameraHelper.getModelValue(UVCCameraHelper.MODE_CONTRAST));
////                        }
//                        Looper.loop();
//                    }
//                }).start();
            }
        }

        @Override
        public void onDisConnectDev(UsbDevice device) {
            showShortMsg("disconnecting");
        }
    };

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_usbcamera);
        ButterKnife.bind(this);

        initView();

        // step.1 initialize UVCCameraHelper
        mUVCCameraView = (CameraViewInterface) mTextureView;
        mUVCCameraView.setCallback(this);
        mCameraHelper = UVCCameraHelper.getInstance();
        mCameraHelper.setDefaultFrameFormat(UVCCameraHelper.FRAME_FORMAT_MJPEG);
        mCameraHelper.initUSBMonitor(this, mUVCCameraView, listener);

        mCameraHelper.setOnPreviewFrameListener(new AbstractUVCCameraHandler.OnPreViewResultListener() {
            @Override
            public void onPreviewResult(byte[] nv21Yuv) {
                Log.d(TAG, "onPreviewResult: "+nv21Yuv.length);
            }
        });
    }

    private void initView() {
        mToolbar.setTitle("");
        setSupportActionBar(mToolbar);

        /**
         * add by lijun
         */
        mTvLight.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View arg0) {
                int lightValue = 0;
                int contrastValue = 0; // 100 80
                int sharpness = 0;
                int saturation = 0;
                int backlight = 0;
                int gain = 0;
                int hue = 0;
                int gamma = 0;

                if(mCameraHelper != null && mCameraHelper.isCameraOpened()) {
                    lightValue = mCameraHelper.getModelValue(UVCCameraHelper.MODE_BRIGHTNESS);
                    contrastValue = mCameraHelper.getModelValue(UVCCameraHelper.MODE_CONTRAST);



//                    sharpness = mCameraHelper.getModelValue(UVCCameraHelper.MODE_SHARPNESS);
//                    saturation = mCameraHelper.getModelValue(UVCCameraHelper.MODE_SATURATION);
//                    backlight = mCameraHelper.getModelValue(UVCCameraHelper.MODE_BACKLIGHT);
//                    gain = mCameraHelper.getModelValue(UVCCameraHelper.MODE_GAIN);
//                    hue = mCameraHelper.getModelValue(UVCCameraHelper.MODE_HUE);
//                    gamma = mCameraHelper.getModelValue(UVCCameraHelper.MODE_GAMMA);
//                    showShortMsg("sharpness:"+String.valueOf(sharpness)+"   saturation:"+String.valueOf(saturation)+"   backlight:"+String.valueOf(backlight)
//                            +"   gain:"+String.valueOf(gain)+"   hue:"+String.valueOf(hue)+"   gamma:"+String.valueOf(gamma)
//                            +"   lightValue:"+String.valueOf(lightValue)+"   contrastValue:"+String.valueOf(contrastValue));
//                    // SHARPNESS 清晰度 50  0 6 3
//                    mCameraHelper.setModelValue(UVCCameraHelper.MODE_SHARPNESS, 3);
//                    // SATURATION 饱和度50  0 128 64
//                    mCameraHelper.setModelValue(UVCCameraHelper.MODE_SATURATION, 64);
//                    // PU_BACKLIGHT 背光补偿0
////                    mCameraHelper.setModelValue(UVCCameraHelper.MODE_BACKLIGHT, 0);
//                    // 增益 0   0 100 0
//                    mCameraHelper.setModelValue(UVCCameraHelper.MODE_GAIN, 15);
//                    // 色调 100 -40 40 0
//                    mCameraHelper.setModelValue(UVCCameraHelper.MODE_HUE, 0);
//                    // 伽马 6   72 500 100
//                    mCameraHelper.setModelValue(UVCCameraHelper.MODE_GAMMA, 500);
//                    // 亮度 100   -64 64 0
//                    mCameraHelper.setModelValue(UVCCameraHelper.MODE_BRIGHTNESS, -64);
//                    // 对比度 80   0 64 32setGain
//                    mCameraHelper.setModelValue(UVCCameraHelper.MODE_CONTRAST, 64);
                }
                settingDialog = new SettingDialog(USBCameraActivity.this, R.style.BottomDialog,
                new SettingDialog.LeaveDialogListener() {
                    @Override
                    public void onClick(View view) {
                        switch(view.getId()){
                            case R.id.iv_back:
                                settingDialog.dismiss();
                            default:
                                break;
                        }
                    }
                },
                new SettingDialog.SeekBarChangedListener() {
                    @Override
                    public void onChange(SeekBar seekBar, int progress, boolean fromUser) {
                        switch(seekBar.getId()){
                            case R.id.sb_light:
                                if(mCameraHelper != null && mCameraHelper.isCameraOpened()) {
                                    mCameraHelper.setModelValue(UVCCameraHelper.MODE_BRIGHTNESS,progress);
                                }
                                break;
                            case R.id.sb_contrast:
                                if(mCameraHelper != null && mCameraHelper.isCameraOpened()) {
                                    mCameraHelper.setModelValue(UVCCameraHelper.MODE_CONTRAST,progress);
                                }
                                break;
                            default:
                                break;
                        }
                    }
                }, lightValue, contrastValue);
                settingDialog.show();
            }
        });
        mTvCamera.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View arg0) {
                if (mCameraHelper == null || !mCameraHelper.isCameraOpened()) {
                    showShortMsg("sorry,camera open failed");
                }
                String picPath = UVCCameraHelper.ROOT_PATH + MyApplication.DIRECTORY_NAME + "/images/"
                        + System.currentTimeMillis() + UVCCameraHelper.SUFFIX_JPEG;
                try {
                    mCameraHelper.capturePicture(picPath, new AbstractUVCCameraHandler.OnCaptureListener() {
                        @Override
                        public void onCaptureResult(String path) {
                            if(TextUtils.isEmpty(path)) {
                                return;
                            }
                            new Handler(getMainLooper()).post(new Runnable() {
                                @Override
                                public void run() {
                                    String result = doParseImage(path);
                                    Toast.makeText(USBCameraActivity.this, result, Toast.LENGTH_LONG).show();
                                }
                            });
                        }
                    });

                }catch (Exception ex){
                    showShortMsg(ex.getMessage());
                }
            }
        });
        mTvResolution.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View arg0) {
                if (mCameraHelper == null || !mCameraHelper.isCameraOpened()) {
                    showShortMsg("sorry,camera open failed");
                }else {
                    showResolutionListDialog();
                }
            }
        });

    }

    private String doParseImage(String path){
        PythonInit pythonInit = new PythonInit();
        pythonInit.init(this);
//        BitmapFactory.Options options = new BitmapFactory.Options();
//        options.inScaled = false;
//        Bitmap bitmap = BitmapFactory.decodeResource(getResources(),R.drawable.test_image, options);
//        String imageString = this.getString(bitmap);
        String imageString = UVCCameraHelper.ROOT_PATH + MyApplication.DIRECTORY_NAME + "/images/ssave.jpg";
//        String picPath = UVCCameraHelper.ROOT_PATH + MyApplication.DIRECTORY_NAME + "/images/"
//                + System.currentTimeMillis() + UVCCameraHelper.SUFFIX_JPEG;
        String result = pythonInit.callImageParse(path, imageString);
        return  result;
    }

    @Override
    protected void onStart() {
        super.onStart();
        // step.2 register USB event broadcast
        if (mCameraHelper != null) {
            mCameraHelper.registerUSB();
        }
    }

    @Override
    protected void onStop() {
        super.onStop();
        // step.3 unregister USB event broadcast
        if (mCameraHelper != null) {
            mCameraHelper.unregisterUSB();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.main_toobar, menu);
        return true;
    }

    private String getString(Bitmap bitmap) {
        ByteArrayOutputStream baos=new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.JPEG,100,baos);
        byte[] byteImage=baos.toByteArray();
        String encoded_image=android.util.Base64.encodeToString(byteImage, Base64.DEFAULT);
        return encoded_image;
    }
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
//        PythonInit pythonInit = new PythonInit();
        switch (item.getItemId()) {
            case R.id.menu_takepic:
//                pythonInit.init(this);
//                BitmapFactory.Options options = new BitmapFactory.Options();
//                options.inScaled = false;
//                Bitmap bitmap = BitmapFactory.decodeResource(getResources(),R.drawable.test_image, options);
//                String imageString = this.getString(bitmap);
//                String picPath = UVCCameraHelper.ROOT_PATH + MyApplication.DIRECTORY_NAME + "/images/"
//                        + System.currentTimeMillis() + UVCCameraHelper.SUFFIX_JPEG;
//                String result = pythonInit.callImageParse(picPath, imageString);
//                Toast.makeText(USBCameraActivity.this, result, Toast.LENGTH_LONG).show();


                if (mCameraHelper == null || !mCameraHelper.isCameraOpened()) {
                    showShortMsg("sorry,camera open failed");
                    return super.onOptionsItemSelected(item);
                }
                String picPath = UVCCameraHelper.ROOT_PATH + MyApplication.DIRECTORY_NAME + "/images/"
                        + System.currentTimeMillis() + UVCCameraHelper.SUFFIX_JPEG;

                mCameraHelper.capturePicture(picPath, new AbstractUVCCameraHandler.OnCaptureListener() {
                    @Override
                    public void onCaptureResult(String path) {
                        if(TextUtils.isEmpty(path)) {
                            return;
                        }
                        new Handler(getMainLooper()).post(new Runnable() {
                            @Override
                            public void run() {
                                Toast.makeText(USBCameraActivity.this, "save path:"+path, Toast.LENGTH_SHORT).show();
                            }
                        });
                    }
                });

                break;
            case R.id.menu_recording:
                if (mCameraHelper == null || !mCameraHelper.isCameraOpened()) {
                    showShortMsg("sorry,camera open failed");
                    return super.onOptionsItemSelected(item);
                }
                if (!mCameraHelper.isPushing()) {
                    String videoPath = UVCCameraHelper.ROOT_PATH + MyApplication.DIRECTORY_NAME +"/videos/" + System.currentTimeMillis()
                            + UVCCameraHelper.SUFFIX_MP4;

//                    FileUtils.createfile(FileUtils.ROOT_PATH + "test666.h264");
                    // if you want to record,please create RecordParams like this
                    RecordParams params = new RecordParams();
                    params.setRecordPath(videoPath);
                    params.setRecordDuration(0);                        // auto divide saved,default 0 means not divided

                    params.setSupportOverlay(true); // overlay only support armeabi-v7a & arm64-v8a
                    mCameraHelper.startPusher(params, new AbstractUVCCameraHandler.OnEncodeResultListener() {
                        @Override
                        public void onEncodeResult(byte[] data, int offset, int length, long timestamp, int type) {
                            // type = 1,h264 video stream
                            if (type == 1) {
                                FileUtils.putFileStream(data, offset, length);
                            }
                            // type = 0,aac audio stream
                            if(type == 0) {

                            }
                        }

                        @Override
                        public void onRecordResult(String videoPath) {
                            if(TextUtils.isEmpty(videoPath)) {
                                return;
                            }
                            new Handler(getMainLooper()).post(() -> Toast.makeText(USBCameraActivity.this, "save videoPath:"+videoPath, Toast.LENGTH_SHORT).show());
                        }
                    });
                    // if you only want to push stream,please call like this
                    // mCameraHelper.startPusher(listener);
                    showShortMsg("start record...");
                } else {
                    FileUtils.releaseFile();
                    mCameraHelper.stopPusher();
                    showShortMsg("stop record...");
                }
                break;
            case R.id.menu_resolution:
                if (mCameraHelper == null || !mCameraHelper.isCameraOpened()) {
                    showShortMsg("sorry,camera open failed");
                    return super.onOptionsItemSelected(item);
                }
                showResolutionListDialog();
                break;
            case R.id.menu_focus:
                if (mCameraHelper == null || !mCameraHelper.isCameraOpened()) {
                    showShortMsg("sorry,camera open failed");
                    return super.onOptionsItemSelected(item);
                }
                mCameraHelper.startCameraFoucs();
                break;
        }
        return super.onOptionsItemSelected(item);
    }

    private void showResolutionListDialog() {
        AlertDialog.Builder builder = new AlertDialog.Builder(USBCameraActivity.this);
        View rootView = LayoutInflater.from(USBCameraActivity.this).inflate(R.layout.layout_dialog_list, null);
        ListView listView = (ListView) rootView.findViewById(R.id.listview_dialog);
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(USBCameraActivity.this, android.R.layout.simple_list_item_1, getResolutionList());
        if (adapter != null) {
            listView.setAdapter(adapter);
        }
        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int position, long id) {
                if (mCameraHelper == null || !mCameraHelper.isCameraOpened())
                    return;
                final String resolution = (String) adapterView.getItemAtPosition(position);
                String[] tmp = resolution.split("x");
                if (tmp != null && tmp.length >= 2) {
                    int widht = Integer.valueOf(tmp[0]);
                    int height = Integer.valueOf(tmp[1]);
                    mCameraHelper.updateResolution(widht, height);
                }
                mDialog.dismiss();
            }
        });

        builder.setView(rootView);
        mDialog = builder.create();
        mDialog.show();
    }

    // example: {640x480,320x240,etc}
    private List<String> getResolutionList() {
        List<Size> list = mCameraHelper.getSupportedPreviewSizes();
        List<String> resolutions = null;
        if (list != null && list.size() != 0) {
            resolutions = new ArrayList<>();
            for (Size size : list) {
                if (size != null) {
                    resolutions.add(size.width + "x" + size.height);
                }
            }
        }
        return resolutions;
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        FileUtils.releaseFile();
        // step.4 release uvc camera resources
        if (mCameraHelper != null) {
            mCameraHelper.release();
        }
    }

    private void showShortMsg(String msg) {
        Toast.makeText(this, msg, Toast.LENGTH_SHORT).show();
    }

    @Override
    public USBMonitor getUSBMonitor() {
        return mCameraHelper.getUSBMonitor();
    }

    @Override
    public void onDialogResult(boolean canceled) {
        if (canceled) {
            showShortMsg("取消操作");
        }
    }

    public boolean isCameraOpened() {
        return mCameraHelper.isCameraOpened();
    }

    @Override
    public void onSurfaceCreated(CameraViewInterface view, Surface surface) {
        if (!isPreview && mCameraHelper.isCameraOpened()) {
            mCameraHelper.startPreview(mUVCCameraView);
            isPreview = true;
        }
    }

    @Override
    public void onSurfaceChanged(CameraViewInterface view, Surface surface, int width, int height) {

    }

    @Override
    public void onSurfaceDestroy(CameraViewInterface view, Surface surface) {
        if (isPreview && mCameraHelper.isCameraOpened()) {
            mCameraHelper.stopPreview();
            isPreview = false;
        }
    }
}
