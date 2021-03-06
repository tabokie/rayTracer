import sys
import operator

__author__ = 'tabokie'

class Color(object):
	def __init__(self,r,g,b,a):
		self.r=r
		self.g=g
		self.b=b
		self.a=a
	@staticmethod
	def H(c):
		upper=max([c.r,c.g,c.b])
		lower=min([c.r,c.g,c.b])
		if upper==lower:
			h=0
		elif upper==c.r:
			h=(c.g-c.b)/(upper-lower)/6.0
			if h<0:
				h+=1
		elif upper==c.g:
			h=(c.b-c.r)/(upper-lower)/6.0+1.0/3
		elif upper==c.b:
			h=(c.r-c.g)/(upper-lower)/6.0+2.0/3
		# print(c.r,c.g,c.b,'->h=',h)
		return h
	@staticmethod
	def S(c):
		upper=max([c.r,c.g,c.b])
		lower=min([c.r,c.g,c.b])
		if upper==lower or upper+lower==0:
			s=0
		elif upper+lower<=1:
			s=(upper-lower)/(upper+lower)
		else:
			s=(upper-lower)/(2-upper-lower)
		# print(c.r,c.g,c.b,'->s=',s)
		return s
	@staticmethod
	def L(c):
		upper=max([c.r,c.g,c.b])
		lower=min([c.r,c.g,c.b])
		l=(upper+lower)/2.0
		# print(c.r,c.g,c.b,'->l=',l)
		return l
	@staticmethod
	def HSL2RGB(h,s,l):
		# print('hsl:',h,s,l)
		q=l*(1+s) if l<0.5 else l+s-l*s
		p=2*l-q
		t=[h+1/3,h,h-1/3]
		for i in range(3):
			if t[i]<0:
				t[i]+=1
			elif t[i]>1:
				t[i]-=1
		f1=(lambda p,q,t: p+(q-p)*6*t)
		f2=(lambda p,q,t: q)
		f3=(lambda p,q,t: p+(q-p)*6*(2/3-t))
		f4=(lambda p,q,t: p)
		rgb=[0,0,0]
		for i in range(3):
			if t[i]<1/6:
				rgb[i]=f1(p,q,t[i])
			elif t[i]<0.5:
				rgb[i]=f2(p,q,t[i])
			elif t[i]<2/3:
				rgb[i]=f3(p,q,t[i])
			else:
				rgb[i]=f4(p,q,t[i])
			if rgb[i]>1 or rgb[i]<0:
				print(h,s,l)
				print(rgb)
				sys.exit(0)
		return rgb
	def _operation(self,other,op):
		r=op(self.r,other.r)
		g=op(self.g,other.g)
		b=op(self.b,other.b)
		a=op(self.a,other.a)
		return Color(r,g,b,a)
	def __add__(self,other):
		return self._operation(other,operator.add)
	def __truediv__(self,deno):
		#numericType=[int,float]
		return Color(self.r/deno,self.g/deno,self.b/deno,self.a/deno)
	def __rmul__(self,k):
		newColor=Color.HSL2RGB(Color.H(self),Color.S(self),Color.L(self)*k)
		# print('rmul:',self.r,self.g,self.b,'*',k,'=',newColor[0],newColor[1],newColor[2])
		return Color(newColor[0],newColor[1],newColor[2],self.a)
	# compose color
	# use other's lightness
	# rgb->hsl->rgb
	def __mul__(self,other):
		# get 
		newColor=Color.HSL2RGB(Color.H(self),Color.S(self),Color.L(other))
		# print('mul:',self.r,self.g,self.b,'*',other.r,other.g,other.b,'=',newColor[0],newColor[1],newColor[2])
		return Color(newColor[0],newColor[1],newColor[2],self.a)
	@staticmethod
	def printColor(c):
		print('R:',int(c.r*255),' G:',int(c.g*255),' B:',int(c.b*255),' A:',int(c.a*255))
		return
	@staticmethod
	def uint32(c):
		return int(c.r*255)<<24|int(c.g*255)<<16|int(c.b*255)<<8|int(c.a*255)
	@staticmethod
	def white():
		return Color(1,1,1,1)
	@staticmethod
	def black():
		return Color(0,0,0,1)
	@staticmethod
	def red():
		return Color(1,0,0,1)
	@staticmethod
	def blue():
		return Color(0,0,1,1)
	@staticmethod
	def zero():
		return Color(0,0,0,0)
	@staticmethod
	def default():
		return Color(0,0,0,1)

