#pragma rtGlobals=1	

function kill_graphs_and_tables()
	string object_name
	variable string_length
	do
		object_name = WinName(0,3)			// name of top graph or table  (see III-441)
		string_length = strlen(object_name)	        // returns "" if no graph/table is present	
		if (string_length == 0)
			break
		endif
		DoWindow /K $object_name			// kill top graph or table; keep going till all done
	while (1)                                                            // loop forever until break		
end