#!/bin/bash

echo 'use s53654__wiki2email; delete from users where confirmed=0' | sql local
