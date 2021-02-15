/* Created by Language version: 7.7.0 */
/* VECTORIZED */
#define NRN_VECTORIZED 1
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "scoplib_ansi.h"
#undef PI
#define nil 0
#include "md1redef.h"
#include "section.h"
#include "nrniv_mf.h"
#include "md2redef.h"
 
#if METHOD3
extern int _method3;
#endif

#if !NRNGPU
#undef exp
#define exp hoc_Exp
extern double hoc_Exp(double);
#endif
 
#define nrn_init _nrn_init__CHR2
#define _nrn_initial _nrn_initial__CHR2
#define nrn_cur _nrn_cur__CHR2
#define _nrn_current _nrn_current__CHR2
#define nrn_jacob _nrn_jacob__CHR2
#define nrn_state _nrn_state__CHR2
#define _net_receive _net_receive__CHR2 
 
#define _threadargscomma_ _p, _ppvar, _thread, _nt,
#define _threadargsprotocomma_ double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt,
#define _threadargs_ _p, _ppvar, _thread, _nt
#define _threadargsproto_ double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg();
 /* Thread safe. No static _p or _ppvar. */
 
#define t _nt->_t
#define dt _nt->_dt
#define N _p[0]
#define e _p[1]
#define lighton _p[2]
#define lightoff _p[3]
#define i _p[4]
#define p _p[5]
#define pmax _p[6]
#define gCHR2 _p[7]
#define ka _p[8]
#define E _p[9]
#define lightdur _p[10]
#define a _p[11]
#define kac _p[12]
#define phi _p[13]
#define v _p[14]
#define _g _p[15]
 
#if MAC
#if !defined(v)
#define v _mlhv
#endif
#if !defined(h)
#define h _mlhh
#endif
#endif
 
#if defined(__cplusplus)
extern "C" {
#endif
 static int hoc_nrnpointerindex =  -1;
 static Datum* _extcall_thread;
 static Prop* _extcall_prop;
 /* external NEURON variables */
 /* declaration of user functions */
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_prop_size(int, int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
extern Memb_func* memb_func;
 
#define NMODL_TEXT 1
#if NMODL_TEXT
static const char* nmodl_file_text;
static const char* nmodl_filename;
extern void hoc_reg_nmodl_text(int, const char*);
extern void hoc_reg_nmodl_filename(int, const char*);
#endif

 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 _extcall_prop = _prop;
 }
 static void _hoc_setdata() {
 Prop *_prop, *hoc_getdata_range(int);
 _prop = hoc_getdata_range(_mechtype);
   _setdata(_prop);
 hoc_retpushx(1.);
}
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 "setdata_CHR2", _hoc_setdata,
 0, 0
};
 /* declare global and static user variables */
#define Sretinal Sretinal_CHR2
 double Sretinal = 1.2e-08;
#define kd kd_CHR2
 double kd = 0.1;
#define lambda lambda_CHR2
 double lambda = 5e-05;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "lighton_CHR2", "ms",
 "lightoff_CHR2", "ms",
 "i_CHR2", "mA/cm2",
 "gCHR2_CHR2", "S/cm2",
 0,0
};
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "lambda_CHR2", &lambda_CHR2,
 "Sretinal_CHR2", &Sretinal_CHR2,
 "kd_CHR2", &kd_CHR2,
 0,0
};
 static DoubVec hoc_vdoub[] = {
 0,0,0
};
 static double _sav_indep;
 static void nrn_alloc(Prop*);
static void  nrn_init(_NrnThread*, _Memb_list*, int);
static void nrn_state(_NrnThread*, _Memb_list*, int);
 static void nrn_cur(_NrnThread*, _Memb_list*, int);
static void  nrn_jacob(_NrnThread*, _Memb_list*, int);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"CHR2",
 "N_CHR2",
 "e_CHR2",
 "lighton_CHR2",
 "lightoff_CHR2",
 0,
 "i_CHR2",
 "p_CHR2",
 "pmax_CHR2",
 "gCHR2_CHR2",
 "ka_CHR2",
 "E_CHR2",
 0,
 0,
 0};
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 16, _prop);
 	/*initialize range parameters*/
 	N = 0;
 	e = 0;
 	lighton = 0;
 	lightoff = 0;
 	_prop->param = _p;
 	_prop->param_size = 16;
 
}
 static void _initlists();
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, _NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _CHR2_reg() {
	int _vectorized = 1;
  _initlists();
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 1);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 16, 0);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 CHR2 /home/yuz615/Bio/githubVersion/accuracyCompare/biophy/modfile/CHR2.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static char *modelname = "CHR2";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  int _i; double _save;{

}
}

static void nrn_init(_NrnThread* _nt, _Memb_list* _ml, int _type){
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v = _v;
 initmodel(_p, _ppvar, _thread, _nt);
}
}

static double _nrn_current(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _v){double _current=0.;v=_v;{ {
   if ( ( t > lighton )  && ( t < lightoff ) ) {
     E = e ;
     }
   else {
     E = 0.0 ;
     }
   lightdur = lightoff - lighton ;
   phi = E * 1e-6 * 1e-3 * 1e-3 * 470e-9 / 6.63e-34 / 3e8 ;
   ka = 0.5 * phi * Sretinal ;
   kac = 0.5 * Sretinal * 10.0 * 1e-6 * 1e-3 * 1e-3 * 470e-9 / 6.63e-34 / 3e8 ;
   pmax = ( kac / ( kac + kd ) - ( kac / ( kac + kd ) * exp ( - ( kac + kd ) * lightdur ) ) ) ;
   if ( e  == 0.0 ) {
     p = 0.0 ;
     }
   else if ( ( t > lighton )  && ( t < lightoff ) ) {
     p = ( ka / ( ka + kd ) - ( ka / ( ka + kd ) * exp ( - ( ka + kd ) * ( t - lighton ) ) ) ) ;
     }
   else if ( t > lightoff ) {
     p = pmax * exp ( - ( t - lightoff ) * kd ) ;
     }
   gCHR2 = p * N * lambda ;
   i = ( 0.1 ) * gCHR2 * v ;
   }
 _current += i;

} return _current;
}

static void nrn_cur(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 _g = _nrn_current(_p, _ppvar, _thread, _nt, _v + .001);
 	{ _rhs = _nrn_current(_p, _ppvar, _thread, _nt, _v);
 	}
 _g = (_g - _rhs)/.001;
#if CACHEVEC
  if (use_cachevec) {
	VEC_RHS(_ni[_iml]) -= _rhs;
  }else
#endif
  {
	NODERHS(_nd) -= _rhs;
  }
 
}
 
}

static void nrn_jacob(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml];
#if CACHEVEC
  if (use_cachevec) {
	VEC_D(_ni[_iml]) += _g;
  }else
#endif
  {
     _nd = _ml->_nodelist[_iml];
	NODED(_nd) += _g;
  }
 
}
 
}

static void nrn_state(_NrnThread* _nt, _Memb_list* _ml, int _type) {

}

static void terminal(){}

static void _initlists(){
 double _x; double* _p = &_x;
 int _i; static int _first = 1;
  if (!_first) return;
_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif

#if NMODL_TEXT
static const char* nmodl_filename = "/home/yuz615/Bio/githubVersion/accuracyCompare/biophy/modfile/CHR2.mod";
static const char* nmodl_file_text = 
  "TITLE CHR2\n"
  "\n"
  "UNITS {\n"
  "	(mV) = (millivolt)\n"
  "	(pA) = (picoamp)\n"
  "	(mA) = (milliamp)\n"
  "	(nS) = (nanosiemens)\n"
  "	(S)  = (siemens)\n"
  "	(mS) = (millisiemens)\n"
  "	(uS) = (microsiemens)\n"
  "}\n"
  "\n"
  "NEURON {\n"
  "	SUFFIX CHR2\n"
  "	RANGE lighton, lightoff, pmax, p, gCHR2, N,e , E, ka\n"
  "	NONSPECIFIC_CURRENT i\n"
  "}\n"
  "\n"
  "INDEPENDENT { t FROM 0 TO 1 WITH 1 (ms) }\n"
  "\n"
  "PARAMETER {\n"
  "	N\n"
  "\n"
  "\n"
  "	lambda = 50e-6\n"
  "	Sretinal = 1.2e-8\n"
  "\n"
  "	kd = 0.1\n"
  "	e\n"
  "	lighton  (ms)\n"
  "	lightoff (ms)\n"
  "}\n"
  "\n"
  "\n"
  "ASSIGNED {\n"
  "	v  (mV)\n"
  "	i  (mA/cm2)\n"
  "	p pmax\n"
  "	lightdur\n"
  "	gCHR2 (S/cm2)\n"
  "	ka a kac\n"
  "	E\n"
  "	phi\n"
  "}\n"
  "\n"
  "BREAKPOINT{\n"
  "\n"
  "	if((t > lighton)&&(t < lightoff)){\n"
  "		E=e\n"
  "	}else{\n"
  "		E=0\n"
  "	}\n"
  "	\n"
  "	lightdur=lightoff-lighton\n"
  "	phi = E*1e-6*1e-3*1e-3*470e-9/6.63e-34/3e8\n"
  "\n"
  "	\n"
  "	ka = 0.5*phi*Sretinal\n"
  "	kac = 0.5*Sretinal*10*1e-6*1e-3*1e-3*470e-9/6.63e-34/3e8\n"
  "\n"
  "	pmax = (kac/(kac+kd) - (kac/(kac+kd)*exp(-(kac+kd)*lightdur)))\n"
  "	\n"
  "	if(e==0){\n"
  "		p=0\n"
  "	}\n"
  "	else if((t > lighton)&&(t < lightoff)){\n"
  "		p = (ka/(ka+kd) - (ka/(ka+kd)*exp(-(ka+kd)*(t-lighton))))\n"
  "	}else if (t > lightoff){\n"
  "		p = pmax*exp(-(t-lightoff)*kd)\n"
  "	}\n"
  "\n"
  "	gCHR2 = p*N*lambda\n"
  "	i = (0.1)*gCHR2 * v\n"
  "}\n"
  "\n"
  ;
#endif
