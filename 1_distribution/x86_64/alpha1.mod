COMMENT
ENDCOMMENT
					       
NEURON {
	POINT_PROCESS alpha1
	RANGE tau, e, i, delay,g
	NONSPECIFIC_CURRENT i
}
UNITS {
	(nA) = (nanoamp)
	(mV) = (millivolt)
	(uS) = (microsiemens)
}

PARAMETER {
	tau=0.1 (ms) <1e-9,1e9>
	e=0	(mV)
	delay=0 (ms)
}

ASSIGNED { 
	ts (ms)
	v (mV) 
	i (nA)  
	g (uS)
	gmax (uS)
}

BREAKPOINT {
	g = alpha( (t - ts)/tau )
	i = g*(v - e)
}

FUNCTION alpha(x) {
	if (x<0 || x>650)	{
		alpha = 0
	}else{
		alpha = gmax * x * exp(-x)
	}
}

NET_RECEIVE(weight (uS)) {
	gmax=weight
	ts=t
}






