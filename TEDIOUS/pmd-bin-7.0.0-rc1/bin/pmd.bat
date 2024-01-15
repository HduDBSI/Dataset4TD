@echo off
set TOPDIR="%~dp0.."
set OPTS=
set COMMAND=%1
set MAIN_CLASS=net.sourceforge.pmd.cli.PmdCli


:: sets the jver variable to the java version, eg 90 for 9.0.1+x or 80 for 1.8.0_171-b11 or 110 for 11.0.6.1
:: sets the jvendor variable to either java (oracle) or openjdk
for /f tokens^=1^,3^,4^,5^ delims^=.-_+^"^  %%j in ('java -version 2^>^&1 ^| findstr /c:"version"') do (
  set jvendor=%%j
  if %%l EQU ea (
    set /A "jver=%%k0"
  ) else (
    if %%k EQU 1 (
      :: for java version 1.7.x, 1.8.x, ignore the first 1.
      set /A "jver=%%l%%m"
    ) else (
      set /A "jver=%%k%%l"
    )
  )
)

Set "jreopts="
:: oracle java 9 and 10 has javafx included as a module
if /I %jvendor% == java (
    if %jver% GEQ 90 (
        if %jver% LSS 110 (
            :: enable reflection
            SETLOCAL EnableDelayedExpansion
            rem java9 and java10 from oracle contain javafx as a module
            rem open internal module of javafx to reflection (for our TreeViewWrapper)
            set "jreopts=--add-opens javafx.controls/javafx.scene.control.skin=ALL-UNNAMED"
            rem The rest here is for RichtextFX
            set "jreopts=!jreopts! --add-opens javafx.graphics/javafx.scene.text=ALL-UNNAMED"
            set "jreopts=!jreopts! --add-opens javafx.graphics/com.sun.javafx.scene.text=ALL-UNNAMED"
            set "jreopts=!jreopts! --add-opens javafx.graphics/com.sun.javafx.text=ALL-UNNAMED"
            set "jreopts=!jreopts! --add-opens javafx.graphics/com.sun.javafx.geom=ALL-UNNAMED"
            rem Warn of remaining illegal accesses
            set "jreopts=!jreopts! --illegal-access=warn"

        )
    )
)

set "_needjfxlib=0"
if [%COMMAND%] == [designer] (
    if /I %jvendor% == openjdk set _needjfxlib=1
    if /I %jvendor% == java (
        if %jver% GEQ 110 set _needjfxlib=1
    )
)
if %_needjfxlib% EQU 1 (
    if %jver% LSS 100 (
        echo For openjfx at least java 10 is required.
        pause
        exit
    )
    if [%JAVAFX_HOME%] EQU [] (
        echo The environment variable JAVAFX_HOME is missing.
        pause
        exit
    )
    :: The wildcard will include only jar files, but we need to access also
    :: property files such as javafx.properties that lay bare in the dir
    set pmd_classpath=%TOPDIR%\conf;%TOPDIR%\lib\*;%JAVAFX_HOME%\lib\*;%JAVAFX_HOME%\lib\
) else (
    set pmd_classpath=%TOPDIR%\conf;%TOPDIR%\lib\*
)

if [%CLASSPATH%] NEQ [] (
    set classpath=%CLASSPATH%;%pmd_classpath%
) else (
    set classpath=%pmd_classpath%
)

java %PMD_JAVA_OPTS% %jreopts% -classpath %pmd_classpath% %OPTS% %MAIN_CLASS% %*
