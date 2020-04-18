#!/bin/bash


alert(){
    osascript -e 'display alert "Battery is low ('$1')"'
}


alert Keyboard
