TITLE CHR2

UNITS {
	(mV) = (millivolt)
	(pA) = (picoamp)
	(mA) = (milliamp)
	(nS) = (nanosiemens)
	(S)  = (siemens)
	(mS) = (millisiemens)
	(uS) = (microsiemens)
}

NEURON {
	SUFFIX CHR2
	RANGE lighton, lightoff, pmax, p, gCHR2, N,e , E, ka
	NONSPECIFIC_CURRENT i
}

INDEPENDENT { t FROM 0 TO 1 WITH 1 (ms) }

PARAMETER {
	N


	lambda = 50e-6
	Sretinal = 1.2e-8

	kd = 0.1
	e
	lighton  (ms)
	lightoff (ms)
}


ASSIGNED {
	v  (mV)
	i  (mA/cm2)
	p pmax
	lightdur
	gCHR2 (S/cm2)
	ka a kac
	E
	phi
}

BREAKPOINT{

	if((t > lighton)&&(t < lightoff)){
		E=e
	}else{
		E=0
	}
	
	lightdur=lightoff-lighton
	phi = E*1e-6*1e-3*1e-3*470e-9/6.63e-34/3e8

	
	ka = 0.5*phi*Sretinal
	kac = 0.5*Sretinal*10*1e-6*1e-3*1e-3*470e-9/6.63e-34/3e8

	pmax = (kac/(kac+kd) - (kac/(kac+kd)*exp(-(kac+kd)*lightdur)))
	
	if(e==0){
		p=0
	}
	else if((t > lighton)&&(t < lightoff)){
		p = (ka/(ka+kd) - (ka/(ka+kd)*exp(-(ka+kd)*(t-lighton))))
	}else if (t > lightoff){
		p = pmax*exp(-(t-lightoff)*kd)
	}

	gCHR2 = p*N*lambda
	i = (0.1)*gCHR2 * v
}

