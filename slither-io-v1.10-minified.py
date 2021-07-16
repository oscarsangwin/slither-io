A7='./Highscore/score.txt'
A6='./Images/background.jpeg'
A5='center'
A4=print
p=None
o='right'
n=str
m=abs
l=len
k=list
d='left'
c=min
b=map
V=max
S=tuple
O=range
H=True
G=False
A=int
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT']='hide'
import pygame as B,math as C,time as I,threading as q,random as P
D=850
E=550
J=255,255,255
r=150,150,150
W=0,0,0
K=255,0,0
e=0,255,0
s=0,0,255
t=255,255,0
u=255,0,255
v=0,255,255
X=22,33,34
def w():
	F.fill(J)
	if L:Z.render()
	else:a.render()
	if B.mouse.get_focused():B.mouse.set_visible(G);F.blit(T,B.mouse.get_pos())
	B.display.update()
def Q(text,x,y,col=W,pos=A5):
	C=pos
	if not N:Y('(loading fonts...)');return
	else:Y()
	B=g.render(text,H,col)
	if C==A5:A=B.get_rect(center=(x,y))
	elif C==d:A=B.get_rect(center=(x,y));A.left=x
	elif C==o:A=B.get_rect(center=(x,y));A.right=x
	F.blit(B,A)
def Y(txt=''):
	if txt:B.display.set_caption(f"Slither.io v1.10.2 - {txt}")
	else:B.display.set_caption('Slither.io v1.10.2')
class x:
	def __init__(A):
		A.space=G;A.slider_pos=D;A.in_transition=G;A.map_x=0;A.map_y=0;A.map_angle=0;A.angle_turn_speed=5;A.map_zoom=150;A.new_map_zoom=100;A.map_width=2000;A.map_height=2000;A.player_speed=5;A.player_speed_boost=8;A.player_length=15;A.player_head_rad=35;A.player_base_col=r;A.collision=G;A.end_game_countdown=p;A.eye_radius=13;A.eye_angle_split=38;A.eye_distance=20;A.background_image=B.image.load(A6);A.border_thickness=15;A.max_agar=200;A.agar=[];A.agar_rad=20
		for C in O(A.max_agar-1):A.gen_new_agar()
		A.trail=[];A.trail_space=20;A.trail.insert(0,(-A.map_x,-A.map_y))
	def gen_new_agar(B,from_small=G,x=p,y=p):
		if not x and not y:x=A(P.randint(0,B.map_width-B.agar_rad*2)-B.map_width/2+A(B.agar_rad));y=A(P.randint(0,B.map_height-B.agar_rad*2)-B.map_height/2+A(B.agar_rad))
		C=P.choice((K,e,s,t,v,u));C=S(b(lambda x:V(x-100,0),C));E=P.randint(0,10)
		if from_small:D=2
		else:D=B.agar_rad
		B.agar.append((x,y,C,E,D))
	def update_trail(A):
		I=A.trail[-1];K=[];L=H
		for J in A.trail:
			if L:B=[-A.map_x,-A.map_y];L=G
			else:
				D=B[0]-J[0];E=B[1]-J[1];F=C.sqrt(D**2+E**2);M=A.trail_space/F
				if F<A.trail_space:B=k(J)
				else:B[0]=B[0]-D*M;B[1]=B[1]-E*M
			K.append(S(B))
		A.trail=K.copy()
		if l(A.trail)<A.player_length:
			D=m(I[0]-A.trail[-1][0]);E=m(I[1]-A.trail[-1][1]);F=C.sqrt(D**2+E**2)
			if F>2:A.trail.append(I)
	def rotate_snake(F,speed):
		J=speed;K=B.mouse.get_pos();L=K[0]-A(D/2);M=K[1]-A(E/2);G=C.degrees(C.atan2(L,M));G=360-(G+180)
		if G!=F.map_angle:
			if G>F.map_angle:H=G-F.map_angle;I=F.map_angle+(360-G)
			elif G<F.map_angle:H=G+(360-F.map_angle);I=F.map_angle-G
			if H<=I:
				if H<=F.angle_turn_speed:F.map_angle=G
				else:F.map_angle=(F.map_angle+F.angle_turn_speed)%360
			elif I<=F.angle_turn_speed:F.map_angle=G
			else:
				F.map_angle-=F.angle_turn_speed
				if F.map_angle<0:F.map_angle+=360
		N=C.sin(C.radians(F.map_angle))*J;O=C.cos(C.radians(F.map_angle))*J;F.map_x-=N;F.map_y+=O
	def update_agar(B):
		D=[]
		for A in B.agar:
			E=-B.map_x-A[0];F=-B.map_y-A[1];G=C.sqrt(E**2+F**2)
			if G<=B.player_head_rad:B.player_length+=1
			elif G<=50:A=k(A);A[0]+=E/5;A[1]+=F/5;D.append(S(A))
			else:A=k(A);A[4]=c(A[4]+2,B.agar_rad);D.append(A)
		B.agar=D.copy()
		for I in O(B.max_agar-l(B.agar)):B.gen_new_agar(from_small=H)
	def update(B,space=G):
		if A(B.slider_pos)!=0 and not B.in_transition:B.slider_pos=A(B.slider_pos/1.12)
		if not B.collision:
			B.space=space
			if B.space:C=B.player_speed_boost
			else:C=B.player_speed
			if not A(B.slider_pos):B.update_trail();B.rotate_snake(C)
			if B.player_length<50:B.new_map_zoom=100
			elif B.player_length<100:B.new_map_zoom=80
			elif B.player_length<200:B.new_map_zoom=60
			else:B.new_map_zoom=40
			B.map_zoom-=(B.map_zoom-B.new_map_zoom)/10;B.check_collision()
		elif B.trail:
			for K in O(A(B.player_length/10)):
				try:
					E,F=B.trail[0];B.trail.pop(0)
					if P.randint(0,2)==0:B.gen_new_agar(from_small=H,x=E,y=F)
				except IndexError:B.trail=[]
		elif not B.end_game_countdown:B.end_game_countdown=I.time()
		elif I.time()-B.end_game_countdown>0.7:
			B.in_transition=H
			if A(B.slider_pos)+1>=D:
				global L;L=G;a.reset();global M,R;R=B.player_length
				if R>M:
					M=R
					with open(A7,'w')as J:J.write(n(M))
			else:B.slider_pos=B.slider_pos+(D-B.slider_pos)/3
		B.update_agar()
	def check_collision(B):
		D,E=B.trail[0];F=A(B.player_head_rad/B.trail_space)+1;F+=1;B.collision=G
		for I in B.trail[F:]:
			J=I[0]-D;K=I[1]-E;L=m(C.sqrt(J**2+K**2))
			if L<B.player_head_rad:B.collision=H;return
		if D+B.border_thickness>B.map_width/2 or D-B.border_thickness<-B.map_width/2:B.collision=H;return
		elif E+B.border_thickness>B.map_height/2 or E-B.border_thickness<-B.map_height/2:B.collision=H;return
	def draw_eyes(G):Q,R=D/2,E/2;I=A(-C.sin(C.radians(G.map_angle+180-G.eye_angle_split))*G.eye_distance*(G.map_zoom/100)+Q);K=A(C.cos(C.radians(G.map_angle+180-G.eye_angle_split))*G.eye_distance*(G.map_zoom/100)+R);L=A(-C.sin(C.radians(G.map_angle+180+G.eye_angle_split))*G.eye_distance*(G.map_zoom/100)+Q);M=A(C.cos(C.radians(G.map_angle+180+G.eye_angle_split))*G.eye_distance*(G.map_zoom/100)+R);B.draw.circle(F,J,(I,K),A(G.eye_radius*(G.map_zoom/100)));B.draw.circle(F,J,(L,M),A(G.eye_radius*(G.map_zoom/100)));N=B.mouse.get_pos();O=N[0]-I;P=N[1]-K;H=C.degrees(C.atan2(O,P));H=360-(H+180);I=A(-C.sin(C.radians(H+180))*(G.eye_distance/4)*(G.map_zoom/100)+I);K=A(C.cos(C.radians(H+180))*(G.eye_distance/4)*(G.map_zoom/100)+K);O=N[0]-L;P=N[1]-M;H=C.degrees(C.atan2(O,P));H=360-(H+180);L=A(-C.sin(C.radians(H+180))*(G.eye_distance/4)*(G.map_zoom/100)+L);M=A(C.cos(C.radians(H+180))*(G.eye_distance/4)*(G.map_zoom/100)+M);B.draw.circle(F,W,(I,K),A(G.eye_radius/1.5*(G.map_zoom/100)));B.draw.circle(F,W,(L,M),A(G.eye_radius/1.5*(G.map_zoom/100)))
	def render(G):
		G.draw_background();G.draw_borders()
		for H in G.agar:M=A(C.sin(I.time()*3+H[3])*35);L=S(b(lambda x:V(c(x+M,255),0),H[2]));G.draw_circle_at(H[0],H[1],H[4],col=L)
		if G.collision:L=K
		else:L=G.player_base_col
		G.draw_snake(base_col=L)
		if not G.collision:G.draw_eyes()
		B.draw.rect(F,J,(0,0,120,30));N=A(A(h.get_fps())/2+1)*2;Q(f"FPS: {n(N)}",10,15,pos=d);B.draw.rect(F,J,(D-185,0,185,30));Q('Length:',D-175,15,pos=d);Q(n(G.player_length),D-10,15,pos=o)
		if G.slider_pos:B.draw.rect(F,X,(0,0,A(G.slider_pos)+1,E))
	def draw_snake(B,base_col=e):
		D=0;E=B.trail
		for F in E[::-1]:D+=1;G=S(b(lambda x:V(c(A(x+C.sin((l(B.trail)-D)/8)*60)+B.space*30,255),0),base_col));B.draw_circle_at(*F,B.player_head_rad,col=G)
	def draw_circle_at(C,pos_x,pos_y,radius,col=K):
		G=A(D/2+(pos_x-D/2)*(C.map_zoom/100)+C.map_x*(C.map_zoom/100))+A(D/2)*C.map_zoom/100;H=A(E/2+(pos_y-E/2)*(C.map_zoom/100)+C.map_y*(C.map_zoom/100))+A(E/2)*C.map_zoom/100;I=A(radius*C.map_zoom/100);G=A(G);H=A(H)
		if G+I>0 and G-I<D and H+I>0 and H-I<E:B.draw.circle(F,col,(A(G),A(H)),I)
	def get_rel_coords(B,x,y):C=A(D/2+(x-D/2)*(B.map_zoom/100)+B.map_x*(B.map_zoom/100))+A(D/2)*B.map_zoom/100;F=A(E/2+(y-E/2)*(B.map_zoom/100)+B.map_y*(B.map_zoom/100))+A(E/2)*B.map_zoom/100;return C,F
	def draw_borders(C):
		G,H=C.get_rel_coords(A(-C.map_width/2),A(-C.map_height/2));B.draw.rect(F,K,(A(G),0,-C.border_thickness,E));G,H=C.get_rel_coords(A(C.map_width/2),A(C.map_height/2));B.draw.rect(F,K,(A(G),0,C.border_thickness,E));G,H=C.get_rel_coords(A(-C.map_width/2),A(-C.map_height/2));B.draw.rect(F,K,(0,A(H),D,-C.border_thickness));G,H=C.get_rel_coords(A(C.map_width/2),A(C.map_height/2));B.draw.rect(F,K,(0,A(H),D,C.border_thickness));J=S(b(lambda x:V(0,x-170),K));G,H=C.get_rel_coords(A(-C.map_width/2),A(-C.map_height/2));I=A(-G-D)
		if I<0:B.draw.rect(F,J,(A(G)-C.border_thickness,0,I,E))
		G,H=C.get_rel_coords(A(C.map_width/2),A(C.map_height/2));I=A(D-G)+1
		if I>0:B.draw.rect(F,J,(A(G)+C.border_thickness,0,I,E))
		G,H=C.get_rel_coords(A(-C.map_width/2),A(-C.map_height/2));I=A(-H-E)
		if I<0:B.draw.rect(F,J,(0,A(H)-C.border_thickness,D,I))
		G,H=C.get_rel_coords(A(C.map_width/2),A(C.map_height/2));I=A(E-H)+1
		if I>0:B.draw.rect(F,J,(0,A(H)+C.border_thickness,D,I))
	def draw_background(C):
		L,M=C.background_image.get_size();N=A(L*(C.map_zoom/100));P=A(M*(C.map_zoom/100));C.blit_image=B.transform.scale(C.background_image,(N,P));G,H=C.blit_image.get_size();Q=A(D/G)+3;K=A(E/H)+3
		for R in O(K):
			for S in O(Q):I=S*G;J=R*H;I+=D/2;J+=E/2;I+=C.map_x*(C.map_zoom/100)%G;J+=C.map_y*(C.map_zoom/100)%H;I-=G*(A(K/2)+1);J-=H*(A(K/2)+1);F.blit(C.blit_image,(A(I),A(J)))
class y:
	def __init__(A):A.music_started=G;A.load_image=B.image.load('./Images/loading.png');A.load_image_size=A.load_image.get_rect()[2:4];A.background=B.image.load(A6);A.background_size=A.background.get_rect()[2:4];A.slither_img=B.image.load('./Images/slither-text.png');A.slither_size=A.slither_img.get_rect()[2:4];A.play_button=B.image.load('./Images/play-button.png');A.play_button_size=A.play_button.get_rect()[2:4];A.play_button_hover=G;A.hover_increase=0;A.nevwin_img=B.image.load('./Images/nevwin-game.png');A.nevwin_img_size=A.nevwin_img.get_rect()[2:4];A.by_name_img=B.image.load('./Images/by-name.png');A.by_name_img_size=A.by_name_img.get_rect()[2:4];A.slider_pos=0;A.in_transition=G
	def reset(A):A.in_transition=G
	def update(C):
		if N:
			if not C.music_started:B.mixer.music.play(-1);C.music_started=H
			F,I=B.mouse.get_pos()
			if F>A(D/2-80)and F<A(D/2+80)and I>A(E/4*2.7-80)and I<A(E/4*2.7+80):
				C.play_button_hover=H
				if B.mouse.get_pressed()[0]and N:C.in_transition=H
				if A(C.slider_pos)+1==D:global L;L=H;global Z;Z=x()
			else:C.play_button_hover=G
			if C.in_transition:C.slider_pos+=(D-C.slider_pos)/3
			else:C.slider_pos=A(C.slider_pos/1.12)
	def render(G):
		if N:
			W=A(D/G.background_size[0])+1;Y=A(E/G.background_size[1])+1
			for L in O(W):
				for P in O(Y):F.blit(G.background,(L*G.background_size[0],P*G.background_size[1]))
			K=B.transform.scale(G.slither_img,(G.slither_size[0]+A(C.sin(I.time()*2)*10),G.slither_size[1]+A(C.sin(I.time()*2)*10)));K=B.transform.rotate(K,C.sin(I.time()*2.1)*2);L=A(D/2);P=A(E/4);S=K.get_rect(center=K.get_rect(center=(L,P)).center);F.blit(K,S.topleft)
			if G.play_button_hover:G.hover_increase=c(G.hover_increase+3,20)
			else:G.hover_increase=V(G.hover_increase-3,0)
			T=B.transform.scale(G.play_button,(A(G.play_button_size[0]/4+G.hover_increase)+A(C.sin(I.time()*1.8)*15),A(G.play_button_size[1]/4+G.hover_increase+A(C.sin(I.time()*1.8)*15))));S=T.get_rect(center=T.get_rect(center=(A(D/2),A(E/4*2.7))).center);F.blit(T,S.topleft);F.blit(G.nevwin_img,(10,E-10-G.nevwin_img_size[1]));F.blit(G.by_name_img,(D-10-G.by_name_img_size[0],E-10-G.by_name_img_size[1]));B.draw.rect(F,J,(A(D/2-230),E-50,460,50));Q(f"Last score: {R}",A(D/2-215),E-25,pos=d);Q(f"High score: {M}",A(D/2+215),E-25,pos=o)
			if G.slider_pos:B.draw.rect(F,X,(0,0,A(G.slider_pos)+1,E))
		else:F.fill(X);H=(I.time()-U)*250;B.draw.arc(F,J,(A(D/2)-100,A(E/2)-100,200,200),C.radians(H),C.radians(H+40));B.draw.arc(F,J,(A(D/2)-100,A(E/2)-100,200,200),C.radians(H+180),C.radians(H+220));H=(I.time()-U)*-250;B.draw.arc(F,J,(A(D/2)-90,A(E/2)-90,180,180),C.radians(H),C.radians(H+40));B.draw.arc(F,J,(A(D/2)-90,A(E/2)-90,180,180),C.radians(H+180),C.radians(H+220));F.blit(G.load_image,(A(D/2-G.load_image_size[0]/2),A(E/2-G.load_image_size[1]/2)))
a=y()
B.init()
Y()
F=B.display.set_mode((D,E))
T=B.image.load('./Images/cursor2.png')
f=T.get_size()
T=B.transform.scale(T,(A(f[0]/5),A(f[1]/5)))
B.mixer.music.load('./Music/sunny.wav')
R=0
with open(A7,'r')as z:
	try:M=A(z.read())
	except ValueError:A4('Failed to load highscore');M=0
N=G
def A0():
	global U,g,N;U=I.time()
	try:
		B.font.init();g=B.font.Font('./Fonts/coolfont2.ttf',23)
		while I.time()-U<3:0
		N=H
	except B.error:A4('Failed to load fonts.')
A1=q.Thread(target=A0)
A1.start()
h=B.time.Clock()
L=G
i=H
A2=0
while i:
	A2+=1;h.tick(60)
	for A3 in B.event.get():
		if A3.type==B.QUIT:i=G
	if B.key.get_pressed()[B.K_SPACE]:j=H
	else:j=G
	if L:Z.update(space=j)
	else:a.update()
	w()
B.quit()
