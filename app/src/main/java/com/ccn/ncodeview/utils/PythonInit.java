package com.ccn.ncodeview.utils;

import android.content.Context;

import com.chaquo.python.Kwarg;
import com.chaquo.python.PyObject;
import com.chaquo.python.android.AndroidPlatform;
import com.chaquo.python.Python;

public class PythonInit extends Exception {

    /**
     * 初始化python环境
     */
    public void init(Context androidplatform){
        if (! Python.isStarted()) {
            Python.start(new AndroidPlatform(androidplatform));
        }
    }

    /**
     * 调用python代码
     * @return
     */
    public String callPythonCode(int a, int b, int c){
        try {
            Python py = Python.getInstance();
            PyObject obj1 = py.getModule("hello").callAttr("add", new Kwarg("a", a), new Kwarg("b", b));
//        PyObject obj1 = py.getModule("hello").callAttr("add", new Kwarg("a", a), new Kwarg("b", b));
            // 将Python返回值换为Java中的Integer类型
            String sum = obj1.toJava(String.class);
            return sum;
        }catch (Exception e){
            return e.getMessage();
        }
    }

    /**
     * 执行图片解析
     * @param imageBase64
     * @return
     */
    public String callImageParse(String path, String imageBase64){
        try {
            Python py = Python.getInstance();
            PyObject obj1 = py.getModule("NCodeParse").callAttr("do_image_parse", new Kwarg("imageBase64", imageBase64), new Kwarg("path", path));
            // 将Python返回值换为Java中的Integer类型
            String result = obj1.toJava(String.class);
            return result;
        }catch (Exception e){
            return e.getMessage();
        }
    }
}
