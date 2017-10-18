#pragma rtGlobals=1	

Function killHighPtsArray(wavetoedit,threshold)
	variable threshold
	wave wavetoedit
	variable rows = DimSize(wavetoedit,0)
	variable columns = DimSize(wavetoedit,1)

	variable i,j
	for (j=0;j<rows;j+=1)
	for (i=0;i<columns;i+=1)
	if (wavetoedit[j][i] >= threshold)
	wavetoedit[j][i] = (wavetoedit[j][i-1] + wavetoedit[j][i+1])/2
	endif
	endfor
	endfor
end