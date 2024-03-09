@echo off
setlocal enabledelayedexpansion

REM モデルディレクトリの基本パスを実行ディレクトリのmodelsサブディレクトリに設定
set "dpath=%~dp0models"

REM Taggerモデルダウンロード

REM Taggerモデルダウンロード
set "MODEL_DIR=%dpath%\tagger"
set "MODEL_ID=SmilingWolf/wd-v1-4-moat-tagger-v2"
set "VARIABLES_FILES=variables.data-00000-of-00001 variables.index"
set "FILES=keras_metadata.pb saved_model.pb selected_tags.csv"

if not exist "%MODEL_DIR%" mkdir "%MODEL_DIR%"
if not exist "%MODEL_DIR%\variables" mkdir "%MODEL_DIR%\variables"

REM 通常のファイルをダウンロード
for %%f in (%FILES%) do (
    set "FILE_PATH=%MODEL_DIR%\%%f"
    if not exist "!FILE_PATH!" (
        curl -L "https://huggingface.co/%MODEL_ID%/resolve/main/%%f" -o "!FILE_PATH!"
        echo Downloaded %%f
    ) else (
        echo %%f already exists.
    )
)

REM variablesフォルダ内のファイルをダウンロード
for %%f in (%VARIABLES_FILES%) do (
    set "FILE_PATH=%MODEL_DIR%\variables\%%f"
    if not exist "!FILE_PATH!" (
        curl -L "https://huggingface.co/%MODEL_ID%/resolve/main/variables/%%f" -o "!FILE_PATH!"
        echo Downloaded variables\%%f
    ) else (
        echo variables\%%f already exists.
    )
)


REM Loraモデルダウンロード
set "MODEL_DIR=%dpath%\Lora"
set "MODEL_ID=tori29umai/SDXL_shadow"
set "FILES=shadow01.safetensors"

if not exist "%MODEL_DIR%" mkdir "%MODEL_DIR%"
for %%f in (%FILES%) do (
    set "FILE_PATH=%MODEL_DIR%\%%f"
    if not exist "!FILE_PATH!" (
        curl -L "https://huggingface.co/%MODEL_ID%/resolve/main/%%f" -o "!FILE_PATH!"
        echo Downloaded %%f
    ) else (
        echo %%f already exists.
    )
)

REM ControlNetモデルダウンロード
set "MODEL_DIR=%dpath%\ControlNet"
set "MODEL_ID=stabilityai/control-lora"
set "FILES=control-lora-canny-rank256.safetensors"

if not exist "%MODEL_DIR%" mkdir "%MODEL_DIR%"
for %%f in (%FILES%) do (
    set "FILE_PATH=%MODEL_DIR%\%%f"
    if not exist "!FILE_PATH!" (
        curl -L "https://huggingface.co/%MODEL_ID%/resolve/main/control-LoRAs-rank256/%%f" -o "!FILE_PATH!"
        echo Downloaded %%f
    ) else (
        echo %%f already exists.
    )
)

REM Stable-diffusionモデルダウンロード
set "MODEL_DIR=%dpath%\Stable-diffusion"
set "MODEL_ID=cagliostrolab/animagine-xl-3.0"
set "FILES=animagine-xl-3.0.safetensors"

if not exist "%MODEL_DIR%" mkdir "%MODEL_DIR%"
for %%f in (%FILES%) do (
    set "FILE_PATH=%MODEL_DIR%\%%f"
    if not exist "!FILE_PATH!" (
        curl -L "https://huggingface.co/%MODEL_ID%/resolve/main/%%f" -o "!FILE_PATH!"
        echo Downloaded %%f
    ) else (
        echo %%f already exists.
    )
)

endlocal

pause