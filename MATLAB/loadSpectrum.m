function spectrum = loadSpectrum(filename)
    m = dlmread(filename);
    
    spectrum = SpectrumInd();
    spectrum.Wavelengths = m(:,1);
    spectrum.Counts = m(:,4);

end