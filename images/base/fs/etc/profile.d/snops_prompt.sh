if [ "$UID" = 0 ]; then
	PS1="[\u@f5-super-netops] [\w] # "
else
	PS1="[\u@f5-super-netops] [\w] $ "
fi
