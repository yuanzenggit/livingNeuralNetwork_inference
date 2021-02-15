#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _alpha1_reg(void);
extern void _cal_reg(void);
extern void _CHR2_reg(void);
extern void _expsyn1_reg(void);
extern void _kcRT03_reg(void);
extern void _kdr_reg(void);
extern void _nafPR_reg(void);
extern void _passiv_reg(void);
extern void _rcadecay_reg(void);
extern void _rkq_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," \"modfile//alpha1.mod\"");
    fprintf(stderr," \"modfile//cal.mod\"");
    fprintf(stderr," \"modfile//CHR2.mod\"");
    fprintf(stderr," \"modfile//expsyn1.mod\"");
    fprintf(stderr," \"modfile//kcRT03.mod\"");
    fprintf(stderr," \"modfile//kdr.mod\"");
    fprintf(stderr," \"modfile//nafPR.mod\"");
    fprintf(stderr," \"modfile//passiv.mod\"");
    fprintf(stderr," \"modfile//rcadecay.mod\"");
    fprintf(stderr," \"modfile//rkq.mod\"");
    fprintf(stderr, "\n");
  }
  _alpha1_reg();
  _cal_reg();
  _CHR2_reg();
  _expsyn1_reg();
  _kcRT03_reg();
  _kdr_reg();
  _nafPR_reg();
  _passiv_reg();
  _rcadecay_reg();
  _rkq_reg();
}
