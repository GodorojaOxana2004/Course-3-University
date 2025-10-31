package com.example.dynamiclib;

public class KeyAlreadyRegisteredException extends RuntimeException {
    public KeyAlreadyRegisteredException(String msg) { super(msg); }
}
