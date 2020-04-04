#kemok pep8 error counter

if [ -f $HOME/.local/bin/pep8 ];
then
   $HOME/.local/bin/pep8 $HOME/.local/bin/pep8 $1  | wc -l
else
echo   "pep8 is not installed, need install it to python 3"
fi
