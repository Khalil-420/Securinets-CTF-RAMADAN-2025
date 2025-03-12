#include"stdio.h"
#include"stdlib.h"
#include"string.h"

int main()
{
	char flag[]="Securinets{damn_z3_Goesss_brrrrrr_gg}";
	srand(0x1337fdae);
	unsigned long int ans = 0;
	for(int i=0;i<strlen(flag);i++)
	{
		ans=0;
		printf("\tif( ");
		for(int j=0;j<strlen(flag);j++)
		{
			unsigned long int coeff;
		        coeff = rand()%1024;
			printf("+ input[%d]*%d ",j,coeff);
			ans = ans + (unsigned long int)flag[j] * coeff;
		}
		printf(" == %d)\n",ans);
	}
	return 0;
}