#pragma rtGlobals=1		// Use modern global access method.

function importPS()
	//call this function to import a PS data file and plot it versus its wavenumber. Using the cursors to select the points,
	//a call to peakFitPS with these points will then print the shift at the bottom of the screen and produce a shifted wave
	
	string path = findPSfile()
	LoadWave/J/D/A=PScalib/K=1/Q path
	
	//get references to each of the waves
	wave column1 = PScalib0
	wave column2 = PScalib1
	wave column3 = PScalib2
	wave column4 = PScalib3
	
	//kill columns 2 and 3
	KillWaves column2,column3
	
	column1 = (10000000/column1)-12579
	
	//rename columns to wavelength and counts
	Rename column1 PScalib_wn
	Rename column4 PScalib_cts
	
	Display PScalib_cts vs PScalib_wn
end

function peakFitPS(begPeak1,endPeak1,begPeak2,endPeak2)
	//This function takes in the starting and end points of the two peaks
	//starting with the peak near 2875, and creates a wave called
	//fullwn_PSCAL. It also prints how much it was shifted.
	
	variable begPeak1
	variable endPeak1
	variable begPeak2
	variable endPeak2

	variable xnaught1
	variable xnaught2
	variable shift

	CurveFit/NTHR=0 lor  PScalib_cts[begPeak1,endPeak1] /X=PScalib_wn /D
	wave W_coef
	xnaught1 =  (W_coef[2]-2850.3)

	CurveFit/NTHR=0 lor  PScalib_cts[begPeak2,endPeak2] /X=PScalib_wn /D 
	wave W_coef
	xnaught2 =  (W_coef[2]-3060.7)
	
	shift = (xnaught1+xnaught2)/2
	print "Shift was " + num2str(shift) + " cm^{-1}"
	
	//start off with calibrated full wave
	make/n=850 fullwn_PSCAL
	fullwn_PSCAL[0]= {4065.28,4062.87,4060.43,4058.03,4055.62,4053.18,4050.78,4048.37,4045.97,4043.53,4041.13,4038.73,4036.33,4033.9,4031.5,4029.1,4026.7,4024.27,4021.87,4019.47,4017.08,4014.68,4012.26,4009.86,4007.47}
	fullwn_PSCAL[25]= {4005.08,4002.69,4000.27,3997.88,3995.48,3993.1,3990.71,3988.32,3985.93,3983.52,3981.13,3978.74,3976.36,3973.98,3971.59,3969.21,3966.83,3964.45,3962.06,3959.68,3957.28,3954.9,3952.52,3950.14}
	fullwn_PSCAL[49]= {3947.77,3945.39,3943.02,3940.64,3938.27,3935.89,3933.52,3931.15,3928.78,3926.67,3924.3,3921.92,3919.55,3917.18,3914.83,3912.46,3910.09,3907.73,3905.35,3902.99,3900.63,3898.26,3895.9,3893.54}
	fullwn_PSCAL[73]= {3891.18,3888.83,3886.48,3884.12,3881.76,3879.4,3877.05,3874.69,3872.35,3869.98,3867.63,3865.28,3862.92,3860.57,3858.23,3855.88,3853.55,3851.2,3848.86,3846.51,3844.17,3841.82,3839.48,3837.14}
	fullwn_PSCAL[97]= {3834.8,3832.46,3830.13,3827.79,3825.45,3823.11,3820.78,3818.45,3816.11,3813.79,3811.45,3809.11,3806.79,3804.45,3802.12,3799.81,3797.48,3795.15,3792.83,3790.61,3788.29,3785.96,3783.63,3781.31}
	fullwn_PSCAL[121]= {3778.98,3776.67,3774.35,3772.02,3769.7,3767.39,3765.08,3762.76,3760.44,3758.13,3755.82,3753.5,3751.19,3748.87,3746.55,3744.25,3741.94,3739.64,3737.33,3735.02,3732.71,3730.4,3728.11,3725.79}
	fullwn_PSCAL[145]= {3723.5,3721.19,3718.89,3716.59,3714.29,3712,3709.7,3707.4,3705.1,3702.8,3700.51,3698.22,3695.92,3693.63,3691.34,3689.06,3686.76,3684.47,3682.19,3679.9,3677.6,3675.32,3673.04,3670.74,3668.47}
	fullwn_PSCAL[170]= {3666.19,3663.9,3661.63,3659.34,3657.04,3654.76,3652.48,3650.2,3647.92,3645.63,3643.36,3641.1,3638.81,3636.54,3634.26,3631.99,3629.73,3627.44,3625.17,3622.9,3620.64,3618.37,3616.1,3613.83,3611.57}
	fullwn_PSCAL[195]= {3609.3,3607.03,3604.78,3602.52,3600.25,3597.99,3595.73,3593.46,3591.21,3588.95,3586.69,3584.44,3582.18,3579.93,3577.68,3575.42,3573.16,3570.92,3568.67,3566.42,3564.16,3561.91,3559.67,3557.43}
	fullwn_PSCAL[219]= {3555.17,3552.93,3550.69,3548.44,3546.2,3543.96,3541.71,3539.47,3537.23,3534.99,3532.75,3530.52,3528.28,3525.89,3523.65,3521.41,3519.17,3516.94,3514.71,3512.47,3510.24,3508.01,3505.78,3503.54}
	fullwn_PSCAL[243]= {3501.31,3499.09,3496.86,3494.63,3492.4,3490.18,3487.96,3485.73,3483.51,3481.28,3479.06,3476.84,3474.61,3472.4,3470.18,3467.96,3465.73,3463.53,3461.3,3459.09,3456.88,3454.67,3452.45,3450.24}
	fullwn_PSCAL[267]= {3448.03,3445.82,3443.61,3441.4,3439.2,3436.98,3434.77,3432.57,3430.36,3428.16,3425.95,3423.75,3421.55,3419.35,3417.15,3414.95,3412.75,3410.55,3408.35,3406.16,3403.96,3401.77,3399.58,3397.09}
	fullwn_PSCAL[291]= {3394.91,3392.71,3390.51,3388.32,3386.13,3383.94,3381.74,3379.55,3377.37,3375.18,3372.99,3370.8,3368.62,3366.43,3364.24,3362.06,3359.88,3357.7,3355.51,3353.33,3351.15,3348.97,3346.79,3344.61}
	fullwn_PSCAL[315]= {3342.43,3340.26,3338.08,3335.91,3333.73,3331.56,3329.39,3327.22,3325.04,3322.88,3320.71,3318.54,3316.37,3314.21,3312.04,3309.87,3307.7,3305.54,3303.37,3301.21,3299.05,3296.89,3294.73,3292.57}
	fullwn_PSCAL[339]= {3290.4,3288.25,3286.09,3283.94,3281.78,3279.62,3277.47,3275.31,3273.16,3271.01,3268.86,3266.71,3264.55,3262.41,3260.25,3258.11,3255.96,3253.82,3251.67,3249.52,3247.38,3245.23,3243.09,3240.95}
	fullwn_PSCAL[363]= {3238.81,3236.66,3234.53,3232.39,3230.25,3228.12,3225.97,3223.84,3221.71,3219.56,3217.44,3215.3,3213.17,3211.03,3208.9,3206.78,3204.64,3202.51,3200.38,3198.25,3196.13,3194,3191.87,3189.76,3187.63}
	fullwn_PSCAL[388]= {3185.51,3183.39,3181.26,3179.15,3177.02,3174.91,3172.78,3170.66,3168.55,3166.43,3164.31,3162.2,3160.08,3157.97,3155.86,3153.74,3151.64,3149.52,3146.73,3144.62,3142.51,3140.4,3138.28,3136.18}
	fullwn_PSCAL[412]= {3134.07,3131.95,3129.85,3127.75,3125.64,3123.53,3121.43,3119.32,3117.22,3115.12,3113.01,3110.91,3108.82,3106.71,3104.62,3102.52,3100.42,3098.32,3096.23,3094.13,3092.04,3089.95,3087.85,3085.76}
	fullwn_PSCAL[436]= {3083.67,3081.58,3079.49,3077.4,3075.31,3073.22,3071.13,3069.05,3066.29,3064.2,3062.11,3060.03,3057.94,3055.85,3053.77,3051.69,3049.61,3047.52,3045.44,3043.36,3041.29,3039.21,3037.13,3035.05}
	fullwn_PSCAL[460]= {3032.97,3030.9,3028.81,3026.74,3024.67,3022.6,3020.53,3018.45,3016.38,3014.31,3012.24,3010.17,3008.1,3006.04,3003.97,3001.9,2999.84,2997.77,2995.71,2993.64,2991.58,2989.52,2987.46,2985.39,2983.34}
	fullwn_PSCAL[485]= {2981.28,2979.22,2977.16,2975.1,2973.05,2970.99,2968.94,2966.88,2964.83,2962.78,2960.72,2958.67,2956.62,2954.57,2952.52,2950.47,2948.42,2945.57,2943.52,2941.47,2939.43,2937.38,2935.34,2933.28}
	fullwn_PSCAL[509]= {2931.24,2929.2,2927.15,2925.11,2923.06,2921.03,2918.98,2916.94,2914.9,2912.86,2910.83,2908.79,2906.76,2904.72,2902.68,2900.64,2898.61,2896.57,2894.55,2892.52,2890.49,2888.45,2886.42,2884.4}
	fullwn_PSCAL[533]= {2882.37,2880.34,2878.31,2876.28,2874.26,2872.23,2870.21,2868.19,2866.17,2864.14,2862.12,2860.1,2858.08,2856.06,2854.04,2852.02,2850,2847.99,2845.97,2843.96,2841.94,2839.93,2837.91,2835.9,2833.88}
	fullwn_PSCAL[558]= {2831.88,2829.87,2826.9,2824.89,2822.87,2820.87,2818.86,2816.85,2814.84,2812.83,2810.83,2808.82,2806.82,2804.81,2802.81,2800.81,2798.8,2796.79,2794.8,2792.8,2790.79,2788.8,2786.8,2784.8,2782.8}
	fullwn_PSCAL[583]= {2780.81,2778.81,2776.81,2774.82,2772.83,2770.83,2768.84,2766.84,2764.85,2762.86,2760.87,2758.88,2756.89,2754.91,2752.92,2750.93,2748.95,2746.95,2744.98,2742.99,2741.01,2739.02,2737.03,2735.05}
	fullwn_PSCAL[607]= {2733.07,2731.1,2729.11,2727.14,2725.16,2723.18,2721.2,2719.23,2717.25,2715.28,2713.3,2710.2,2708.22,2706.24,2704.27,2702.29,2700.32,2698.35,2696.38,2694.41,2692.42,2690.47,2688.5,2686.53,2684.57}
	fullwn_PSCAL[632]= {2682.59,2680.63,2678.66,2676.69,2674.74,2672.78,2670.8,2668.84,2666.88,2664.92,2662.96,2661.01,2659.04,2657.09,2655.13,2653.17,2651.21,2649.26,2647.3,2645.35,2643.39,2641.44,2639.49,2637.54}
	fullwn_PSCAL[656]= {2635.58,2633.63,2631.69,2629.74,2627.79,2625.84,2623.89,2621.94,2620,2618.05,2616.11,2614.16,2612.22,2610.27,2608.34,2606.39,2604.46,2602.51,2600.57,2598.63,2595.26,2593.31,2591.38,2589.43}
	fullwn_PSCAL[680]= {2587.5,2585.57,2583.63,2581.69,2579.75,2577.82,2575.88,2573.95,2572.02,2570.09,2568.16,2566.23,2564.29,2562.37,2560.43,2558.5,2556.58,2554.64,2552.72,2550.8,2548.86,2546.94,2545.02,2543.1,2541.17}
	fullwn_PSCAL[705]= {2539.25,2537.32,2535.41,2533.49,2531.57,2529.65,2527.72,2525.81,2523.89,2521.97,2520.06,2518.14,2516.23,2514.32,2512.4,2510.49,2508.58,2506.67,2504.75,2502.84,2500.94,2499.02,2497.11,2495.2}
	fullwn_PSCAL[729]= {2493.29,2491.4,2489.49,2487.58,2485.68,2481.4,2479.49,2477.59,2475.69,2473.78,2471.88,2469.98,2468.07,2466.17,2464.27,2462.37,2460.47,2458.57,2456.67,2454.77,2452.88,2450.98,2449.08,2447.18}
	fullwn_PSCAL[753]= {2445.29,2443.39,2441.5,2439.6,2437.71,2435.81,2433.92,2432.03,2430.13,2428.24,2426.35,2424.46,2422.57,2420.7,2418.81,2416.92,2415.03,2413.14,2411.26,2409.37,2407.48,2405.62,2403.73,2401.85}
	fullwn_PSCAL[777]= {2399.96,2398.08,2396.19,2394.33,2392.45,2390.57,2388.68,2386.83,2384.94,2383.06,2381.18,2379.3,2377.45,2375.57,2373.69,2371.81,2369.96,2368.08,2366.2,2364.35,2362.47,2360.6,2358.75,2356.87}
	fullwn_PSCAL[801]= {2355,2353.13,2351.28,2349.4,2347.55,2345.68,2343.81,2341.96,2340.09,2338.22,2336.38,2334.51,2332.66,2330.8,2328.93,2327.08,2325.22,2323.37,2321.51,2319.67,2317.8,2315.94,2314.1,2312.23,2310.39}
	fullwn_PSCAL[826]= {2308.53,2306.69,2304.83,2302.99,2301.13,2299.3,2297.44,2295.6,2293.74,2291.91,2290.07,2288.21,2286.38,2284.52,2282.69,2280.83,2279,2277.17,2275.32,2273.49,2271.63,2269.8,2267.97,2266.12}
	
	fullwn_PSCAL = fullwn_PSCAL - shift;
	Edit fullwn_PSCAL
end


function/S findPSfile()
	//function for user to select PS calib file and return string of path to it. called by importPS()

	string message = "SelectPS file: " //message at top of prompt
	string outputPath //string variable to store path
	String fileFilters = "Data Files (*.txt,*.dat,*.csv):.txt,.dat,.csv;All Files:.*;" //restrict to data files
	
	Open /D/R /F=fileFilters /M=message refNum //run dialog
	outputPath = S_fileName  //store output path
	
	if(strlen(outputPath) == 0)
		Print "Cancelled by user or file not found."
	endif
	
	return outputPath
end
	
	
	


Function importDFGs(name)
	//main function for importing DFGs.

	string name
	
	string list
	list = selectDFGfiles()
	
	loadDFGtopas(list,name)
	
	backgroundSubtractDFG(list,name)
end

Function/S selectDFGfiles()
	//Line marked below may need to change depending on whether it is a windows or mac computer
	//creates a dialog box that allows the user to select the list of different spectra he/she would
	//like to compile into a single spectrum and outputs a list where the first item is the file path
	//and the rest are the files selected
	
	Variable refNum
	String message = "Select files:" //message at top of prompt
	String outputPaths
	String fileFilters = "Data Files (*.txt,*.dat,*.csv):.txt,.dat,.csv;All Files:.*;"
	Open /D /R /MULT=1 /F=fileFilters /M=message refNum
	outputPaths = S_fileName
	if (strlen(outputPaths) == 0)
		Print "Cancelled"
	else
		string folderName
		string firstPath = StringFromList(0,outputPaths,"\r")
		folderName = ParseFilePath(1,firstPath,":",1,0) //may need to change ":" on windows: "//"?
		
		string DFGlist = folderName + ";"
		Variable numFilesSelected = ItemsInList(outputPaths, "\r")
		Variable i
		for(i=0; i<numFilesSelected; i+=1)
			String path = StringFromList(i, outputPaths, "\r")
			String name = ParseFilePath(3,path,":",1,0)
			DFGlist = DFGlist + name + ";"
			
		endfor
	endif
	return DFGlist // Will be empty if user canceled

End

function loadDFGtopas(list,name)
	//take in list where first entry is path and next items are names of waves to import
	//load waves into IGOR
	string list
	string name
	
	string path = StringFromList(0,list) //path is first item in list
	variable numItems = ItemsInList(list) - 1; //calculate number of files (minus 1 for path)
	
	variable i
	string fileName
	string fullPath 
	string fullName

	
	for (i=1;i<numItems+1;i+=1)
		fileName = StringFromList(i,list)
		fullPath = path + fileName + ".txt";
		fullName = name +"_RAW_" + fileName + "_";
		LoadWave/J/D/A=$fullName/K=1/Q fullPath
		
		//get references to each of the waves
		wave column1 = $(fullName + "0")
		wave column2 = $(fullName + "1")
		wave column3 = $(fullName + "2")
		wave column4 = $(fullName + "3")
		
		//kill columns 2 and 3
		KillWaves column2,column3
		
		
		//rename columns to wavelength and counts
		string wvName = fullName + "wv"
		Rename column1 $wvName
		string countsName = fullName + "cts"
		Rename column4 $countsName
		
	endfor
	

end

Function backgroundSubtractDFG(list,name)
	//background subtracts each individaul DFG as well as pads zeroes on either side and sums
	string list
	string name
	
		
	string fullwnWname = name + "_FULL_wn"
	make/N=850 $fullwnWname
	wave fullwn = $fullwnWname
	fullwn[0]= {4065.28,4062.87,4060.43,4058.03,4055.62,4053.18,4050.78,4048.37,4045.97,4043.53,4041.13,4038.73,4036.33,4033.9,4031.5,4029.1,4026.7,4024.27,4021.87,4019.47,4017.08,4014.68,4012.26,4009.86,4007.47}
	fullwn[25]= {4005.08,4002.69,4000.27,3997.88,3995.48,3993.1,3990.71,3988.32,3985.93,3983.52,3981.13,3978.74,3976.36,3973.98,3971.59,3969.21,3966.83,3964.45,3962.06,3959.68,3957.28,3954.9,3952.52,3950.14}
	fullwn[49]= {3947.77,3945.39,3943.02,3940.64,3938.27,3935.89,3933.52,3931.15,3928.78,3926.67,3924.3,3921.92,3919.55,3917.18,3914.83,3912.46,3910.09,3907.73,3905.35,3902.99,3900.63,3898.26,3895.9,3893.54}
	fullwn[73]= {3891.18,3888.83,3886.48,3884.12,3881.76,3879.4,3877.05,3874.69,3872.35,3869.98,3867.63,3865.28,3862.92,3860.57,3858.23,3855.88,3853.55,3851.2,3848.86,3846.51,3844.17,3841.82,3839.48,3837.14}
	fullwn[97]= {3834.8,3832.46,3830.13,3827.79,3825.45,3823.11,3820.78,3818.45,3816.11,3813.79,3811.45,3809.11,3806.79,3804.45,3802.12,3799.81,3797.48,3795.15,3792.83,3790.61,3788.29,3785.96,3783.63,3781.31}
	fullwn[121]= {3778.98,3776.67,3774.35,3772.02,3769.7,3767.39,3765.08,3762.76,3760.44,3758.13,3755.82,3753.5,3751.19,3748.87,3746.55,3744.25,3741.94,3739.64,3737.33,3735.02,3732.71,3730.4,3728.11,3725.79}
	fullwn[145]= {3723.5,3721.19,3718.89,3716.59,3714.29,3712,3709.7,3707.4,3705.1,3702.8,3700.51,3698.22,3695.92,3693.63,3691.34,3689.06,3686.76,3684.47,3682.19,3679.9,3677.6,3675.32,3673.04,3670.74,3668.47}
	fullwn[170]= {3666.19,3663.9,3661.63,3659.34,3657.04,3654.76,3652.48,3650.2,3647.92,3645.63,3643.36,3641.1,3638.81,3636.54,3634.26,3631.99,3629.73,3627.44,3625.17,3622.9,3620.64,3618.37,3616.1,3613.83,3611.57}
	fullwn[195]= {3609.3,3607.03,3604.78,3602.52,3600.25,3597.99,3595.73,3593.46,3591.21,3588.95,3586.69,3584.44,3582.18,3579.93,3577.68,3575.42,3573.16,3570.92,3568.67,3566.42,3564.16,3561.91,3559.67,3557.43}
	fullwn[219]= {3555.17,3552.93,3550.69,3548.44,3546.2,3543.96,3541.71,3539.47,3537.23,3534.99,3532.75,3530.52,3528.28,3525.89,3523.65,3521.41,3519.17,3516.94,3514.71,3512.47,3510.24,3508.01,3505.78,3503.54}
	fullwn[243]= {3501.31,3499.09,3496.86,3494.63,3492.4,3490.18,3487.96,3485.73,3483.51,3481.28,3479.06,3476.84,3474.61,3472.4,3470.18,3467.96,3465.73,3463.53,3461.3,3459.09,3456.88,3454.67,3452.45,3450.24}
	fullwn[267]= {3448.03,3445.82,3443.61,3441.4,3439.2,3436.98,3434.77,3432.57,3430.36,3428.16,3425.95,3423.75,3421.55,3419.35,3417.15,3414.95,3412.75,3410.55,3408.35,3406.16,3403.96,3401.77,3399.58,3397.09}
	fullwn[291]= {3394.91,3392.71,3390.51,3388.32,3386.13,3383.94,3381.74,3379.55,3377.37,3375.18,3372.99,3370.8,3368.62,3366.43,3364.24,3362.06,3359.88,3357.7,3355.51,3353.33,3351.15,3348.97,3346.79,3344.61}
	fullwn[315]= {3342.43,3340.26,3338.08,3335.91,3333.73,3331.56,3329.39,3327.22,3325.04,3322.88,3320.71,3318.54,3316.37,3314.21,3312.04,3309.87,3307.7,3305.54,3303.37,3301.21,3299.05,3296.89,3294.73,3292.57}
	fullwn[339]= {3290.4,3288.25,3286.09,3283.94,3281.78,3279.62,3277.47,3275.31,3273.16,3271.01,3268.86,3266.71,3264.55,3262.41,3260.25,3258.11,3255.96,3253.82,3251.67,3249.52,3247.38,3245.23,3243.09,3240.95}
	fullwn[363]= {3238.81,3236.66,3234.53,3232.39,3230.25,3228.12,3225.97,3223.84,3221.71,3219.56,3217.44,3215.3,3213.17,3211.03,3208.9,3206.78,3204.64,3202.51,3200.38,3198.25,3196.13,3194,3191.87,3189.76,3187.63}
	fullwn[388]= {3185.51,3183.39,3181.26,3179.15,3177.02,3174.91,3172.78,3170.66,3168.55,3166.43,3164.31,3162.2,3160.08,3157.97,3155.86,3153.74,3151.64,3149.52,3146.73,3144.62,3142.51,3140.4,3138.28,3136.18}
	fullwn[412]= {3134.07,3131.95,3129.85,3127.75,3125.64,3123.53,3121.43,3119.32,3117.22,3115.12,3113.01,3110.91,3108.82,3106.71,3104.62,3102.52,3100.42,3098.32,3096.23,3094.13,3092.04,3089.95,3087.85,3085.76}
	fullwn[436]= {3083.67,3081.58,3079.49,3077.4,3075.31,3073.22,3071.13,3069.05,3066.29,3064.2,3062.11,3060.03,3057.94,3055.85,3053.77,3051.69,3049.61,3047.52,3045.44,3043.36,3041.29,3039.21,3037.13,3035.05}
	fullwn[460]= {3032.97,3030.9,3028.81,3026.74,3024.67,3022.6,3020.53,3018.45,3016.38,3014.31,3012.24,3010.17,3008.1,3006.04,3003.97,3001.9,2999.84,2997.77,2995.71,2993.64,2991.58,2989.52,2987.46,2985.39,2983.34}
	fullwn[485]= {2981.28,2979.22,2977.16,2975.1,2973.05,2970.99,2968.94,2966.88,2964.83,2962.78,2960.72,2958.67,2956.62,2954.57,2952.52,2950.47,2948.42,2945.57,2943.52,2941.47,2939.43,2937.38,2935.34,2933.28}
	fullwn[509]= {2931.24,2929.2,2927.15,2925.11,2923.06,2921.03,2918.98,2916.94,2914.9,2912.86,2910.83,2908.79,2906.76,2904.72,2902.68,2900.64,2898.61,2896.57,2894.55,2892.52,2890.49,2888.45,2886.42,2884.4}
	fullwn[533]= {2882.37,2880.34,2878.31,2876.28,2874.26,2872.23,2870.21,2868.19,2866.17,2864.14,2862.12,2860.1,2858.08,2856.06,2854.04,2852.02,2850,2847.99,2845.97,2843.96,2841.94,2839.93,2837.91,2835.9,2833.88}
	fullwn[558]= {2831.88,2829.87,2826.9,2824.89,2822.87,2820.87,2818.86,2816.85,2814.84,2812.83,2810.83,2808.82,2806.82,2804.81,2802.81,2800.81,2798.8,2796.79,2794.8,2792.8,2790.79,2788.8,2786.8,2784.8,2782.8}
	fullwn[583]= {2780.81,2778.81,2776.81,2774.82,2772.83,2770.83,2768.84,2766.84,2764.85,2762.86,2760.87,2758.88,2756.89,2754.91,2752.92,2750.93,2748.95,2746.95,2744.98,2742.99,2741.01,2739.02,2737.03,2735.05}
	fullwn[607]= {2733.07,2731.1,2729.11,2727.14,2725.16,2723.18,2721.2,2719.23,2717.25,2715.28,2713.3,2710.2,2708.22,2706.24,2704.27,2702.29,2700.32,2698.35,2696.38,2694.41,2692.42,2690.47,2688.5,2686.53,2684.57}
	fullwn[632]= {2682.59,2680.63,2678.66,2676.69,2674.74,2672.78,2670.8,2668.84,2666.88,2664.92,2662.96,2661.01,2659.04,2657.09,2655.13,2653.17,2651.21,2649.26,2647.3,2645.35,2643.39,2641.44,2639.49,2637.54}
	fullwn[656]= {2635.58,2633.63,2631.69,2629.74,2627.79,2625.84,2623.89,2621.94,2620,2618.05,2616.11,2614.16,2612.22,2610.27,2608.34,2606.39,2604.46,2602.51,2600.57,2598.63,2595.26,2593.31,2591.38,2589.43}
	fullwn[680]= {2587.5,2585.57,2583.63,2581.69,2579.75,2577.82,2575.88,2573.95,2572.02,2570.09,2568.16,2566.23,2564.29,2562.37,2560.43,2558.5,2556.58,2554.64,2552.72,2550.8,2548.86,2546.94,2545.02,2543.1,2541.17}
	fullwn[705]= {2539.25,2537.32,2535.41,2533.49,2531.57,2529.65,2527.72,2525.81,2523.89,2521.97,2520.06,2518.14,2516.23,2514.32,2512.4,2510.49,2508.58,2506.67,2504.75,2502.84,2500.94,2499.02,2497.11,2495.2}
	fullwn[729]= {2493.29,2491.4,2489.49,2487.58,2485.68,2481.4,2479.49,2477.59,2475.69,2473.78,2471.88,2469.98,2468.07,2466.17,2464.27,2462.37,2460.47,2458.57,2456.67,2454.77,2452.88,2450.98,2449.08,2447.18}
	fullwn[753]= {2445.29,2443.39,2441.5,2439.6,2437.71,2435.81,2433.92,2432.03,2430.13,2428.24,2426.35,2424.46,2422.57,2420.7,2418.81,2416.92,2415.03,2413.14,2411.26,2409.37,2407.48,2405.62,2403.73,2401.85}
	fullwn[777]= {2399.96,2398.08,2396.19,2394.33,2392.45,2390.57,2388.68,2386.83,2384.94,2383.06,2381.18,2379.3,2377.45,2375.57,2373.69,2371.81,2369.96,2368.08,2366.2,2364.35,2362.47,2360.6,2358.75,2356.87}
	fullwn[801]= {2355,2353.13,2351.28,2349.4,2347.55,2345.68,2343.81,2341.96,2340.09,2338.22,2336.38,2334.51,2332.66,2330.8,2328.93,2327.08,2325.22,2323.37,2321.51,2319.67,2317.8,2315.94,2314.1,2312.23,2310.39}
	fullwn[826]= {2308.53,2306.69,2304.83,2302.99,2301.13,2299.3,2297.44,2295.6,2293.74,2291.91,2290.07,2288.21,2286.38,2284.52,2282.69,2280.83,2279,2277.17,2275.32,2273.49,2271.63,2269.8,2267.97,2266.12}
	
	string sumWname = name +"_FULL_SUM_cts"
	make/N=850 $sumWname
	wave sumwave = $sumWname
	Display sumwave vs fullwn
	SetAxis bottom 4065,2266
	
	Display //figure to add other things to

	
	Edit //table to add to
	
	variable numItems = ItemsInList(list) - 1; //calculate number of files (minus 1 for path)
	
	variable i,j
	variable length
	for (i=1;i<numItems+1;i+=1) //iterate through each file
		string DFGname = StringFromList(i,list) 

		string rawWname
		string newWname
		string bgWname
		string wvWname
		string wnWname
		string fullWname
		string fullindwnname

	
		string possibleBG
	
		if (strsearch(DFGname,"bg",0) < 0) //if it doesn't contain bg, execute everything
	
			rawWname = name +  "_RAW_" + DFGname + "_cts"
			newWname = name + "_BGSUB_" + DFGname + "_cts"
			wvWname = name + "_RAW_" + DFGname + "_wv"
			wnWname = name + "_" + DFGname + "_wn"
			fullWname = name + "_FULL_" + DFGname + "_cts"
			fullindwnname = name + "_FULLWN_" + DFGname + "_wn"
			
			
	
			wave raw = $rawWname
			wave wv = $wvWname
	
			length = numpnts(raw)
			make/N=(length) $newWname
			wave bgsub = $newWname
				
			make/N=(length) $wnWname
			wave wn = $wnWname
			wn = (10000000/wv)-12579
			
			Duplicate wn,$fullindwnname
			wave fullindwn = $fullindwnname

	
			

		
			//written out in case structure for padding zeros on either side, different for most DFGs. 
			//could collapse into loop	
			strswitch(DFGname) 
				case "3600":
			
					for (j=1;j<numItems+1;j+=1)
						possibleBG = StringFromList(j,list)
					
						if ((cmpstr(possibleBG,"3600_bg") == 0 )||(cmpstr(possibleBG,"3500_bg") == 0 ))
							break
						endif
					endfor
				
					bgWname = name + "_RAW_" + possibleBG +  "_cts"
					wave bg = $bgWname
					bgsub = raw-bg
				
					Duplicate bgsub, $fullWname
					wave full = $fullWname
					
					InsertPoints 0,406, full			
					InsertPoints 0,406, fullindwn

					break
				case "3500":
				
					for (j=1;j<numItems+1;j+=1)
						possibleBG = StringFromList(j,list)
					
						if ((cmpstr(possibleBG,"3600_bg") == 0 )||(cmpstr(possibleBG,"3500_bg") == 0 ))
							break
						endif
					endfor
				
					bgWname = name + "_RAW_" + possibleBG +  "_cts"
					wave bg = $bgWname
					bgsub = raw-bg
				
					Duplicate bgsub, $fullWname
					wave full = $fullWname
					InsertPoints 0,406, full
					InsertPoints 0,406, fullindwn
				
				
					break
				case "3400":
					for (j=1;j<numItems+1;j+=1)
						possibleBG = StringFromList(j,list)
					
						if ((cmpstr(possibleBG,"3400_bg") == 0 )||(cmpstr(possibleBG,"3300_bg") == 0 )||(cmpstr(possibleBG,"3200_bg") == 0 ))
							break
						endif
					endfor
				
					bgWname = name + "_RAW_" + possibleBG +  "_cts"
					wave bg = $bgWname
					bgsub = raw-bg
				
					Duplicate bgsub, $fullWname
					wave full = $fullWname
					InsertPoints 0,290, full
					InsertPoints 734,116, full	
					InsertPoints 0,290, fullindwn
					InsertPoints 734,116, fullindwn	
				
					break
				case "3300":
				
					for (j=1;j<numItems+1;j+=1)
						possibleBG = StringFromList(j,list)
					
						if ((cmpstr(possibleBG,"3400_bg") == 0 )||(cmpstr(possibleBG,"3300_bg") == 0 )||(cmpstr(possibleBG,"3200_bg") == 0 ))
							break
						endif
					endfor
				
					bgWname = name + "_RAW_" + possibleBG +  "_cts"
					wave bg = $bgWname
					bgsub = raw-bg
				
					Duplicate bgsub, $fullWname
					wave full = $fullWname
					InsertPoints 0,290, full
					InsertPoints 734,116, full
					InsertPoints 0,290, fullindwn
					InsertPoints 734,116, fullindwn
				
					break
				case "3200":
				
					for (j=1;j<numItems+1;j+=1)
						possibleBG = StringFromList(j,list)
					
						if ((cmpstr(possibleBG,"3400_bg") == 0 )||(cmpstr(possibleBG,"3300_bg") == 0 )||(cmpstr(possibleBG,"3200_bg") == 0 ))
							break
						endif
					endfor
					
					bgWname = name + "_RAW_" + possibleBG +  "_cts"
					wave bg = $bgWname
					bgsub = raw-bg
				
					Duplicate bgsub, $fullWname
					wave full = $fullWname
					InsertPoints 0,290, full
					InsertPoints 734,116, full
					InsertPoints 0,290, fullindwn
					InsertPoints 734,116, fullindwn				
				
					break
				case "3100":		
					bgWname = name + "_RAW_3100_bg_cts"
					wave bg = $bgWname
					bgsub = raw -bg
				
					Duplicate bgsub, $fullWname
					wave full = $fullWname
					InsertPoints 0,232, full
					InsertPoints 676,174, full
					InsertPoints 0,232, fullindwn
					InsertPoints 676,174, fullindwn
				
					break
				case "3000":
				
					bgWname = name + "_RAW_3000_bg_cts"
					wave bg = $bgWname
					bgsub = raw -bg
				
					Duplicate bgsub,$fullWname
					wave full = $fullWname
					InsertPoints 0,174, full
					InsertPoints 618,232, full
					InsertPoints 0,174, fullindwn
					InsertPoints 618,232, fullindwn
							
					break
				case "2900":
				
					bgWname = name + "_RAW_2900_bg_cts"
					wave bg = $bgWname		
					bgsub = raw -bg
				
					Duplicate bgsub, $fullWname
					wave full = $fullWname
					InsertPoints 0,116, full
					InsertPoints 560,290, full
					InsertPoints 0,116, fullindwn
					InsertPoints 560,290, fullindwn
				
				
					break
				case "2800":
				
					bgWname = name + "_RAW_2800_bg_cts"
					wave bg = $bgWname	
					bgsub = raw -bg
				
					Duplicate bgsub, $fullWname
					wave full = $fullWname
					InsertPoints 0,58, full
					InsertPoints 502,348, full
					InsertPoints 0,58, fullindwn
					InsertPoints 502,348, fullindwn
				
					break

				case "2700":

				
					bgWname = name + "_RAW_2700_bg_cts"
					wave bg = $bgWname	
					bgsub = raw -bg
				
					Duplicate bgsub, $fullWname
					wave full = $fullWname
					InsertPoints 444,406, full
					InsertPoints 444,406, fullindwn

				
					break
				default:
					break //if its background ignore
		
			endswitch
			
			sumwave = sumwave + full
			AppendToGraph full vs fullwn
			AppendToTable fullindwn,full	
		
		else

		endif
		
	endfor
	SetAxis bottom 4065,2266
	Edit fullwn,sumwave
	

end


		
	

	
	
	
	
	
	