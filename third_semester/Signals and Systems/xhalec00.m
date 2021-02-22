% Author: Viktoria Haleckova <xhalec00@stud.fit.vutbr.cz>
%1)
[s, Fs] = audioread ('xhalec00.wav'); s= s';
dlzka = length(s);
pocet_s = dlzka/16;
t = dlzka / Fs;

str = sprintf('Dlzka: %d vzoriek, %d s. Vzorkovacia frekvencia je %d Hz. Pocet reprezentovanych binarnych symbolov je %d',dlzka,t,Fs,pocet_s);
disp(str)

%2)
q = [];
j = 1;
for i = 8:16:dlzka
if s(i) > 0
q(j) = 1;
j = j + 1;
else
q(j) = 0;
j = j + 1;
end
end

%XOR
u = textread('xhalec00.txt')
err = 0;
for i = 1:2000
o = u(i);
b = q(i);
if (o == 0 && b == 1)
err = err + 1;
else
err = err;
end
if (o == 1 && b == 0)
err = err + 1;
else
err = err;
end
end

%err == 0 -> no mistakes!

hold on
plot(s(1:Fs/50))
stem((1:20)*16-8,q(1:20))
hold off
axis([wf 320 -1 1]);



%3)
% zeros
B = [0.0192 -0.0185 -0.0185 0.0192];

%poles 
A = [1.0000 -2.8870 2.7997 -0.9113];
if abs(roots(A)) < 1
    disp('Filter je stabilny');
else
    disp('Filter je nestabilny');
end
zplane(roots(B),roots(A));

%4)
k = 256;
H = freqz(B,A,k);
fr2=(0:k-1) / k * Fs / 2; 
plot(fr2,abs(H));
xlabel('f [Hz]'); grid;

%5)
filtered = filter(B, A, s);

hold on
plot(s(1:Fs/50))
plot(filtered(1:Fs/50))
hold off
axis([wf 320 -1 1]);

%6)
e = [];
e = zeros(size(filtered));
e(1:end-16) = filtered(16+1:end);
arr = [];
j = 1;
for i = 8:16:dlzka
if e(i) > 0
arr(j) = 1;
j = j + 1;
else
arr(j) = 0;
j = j + 1;
end
end

hold on
plot(s(1:Fs/50))
plot(filtered(1:Fs/50))
plot(e(1:Fs/50))
stem((1:20)*16-8,arr(1:20))
hold off
axis([wf 320 -1 1]);

%7)
ch = 0;
for i = 1:2000
o = arr(i);
b = q(i);
if (o == 0 && b == 1)
ch = ch + 1;
else
ch = ch;
end
if (o == 1 && b == 0)
ch = ch + 1;
else
ch = ch;
end
end

%8)
frekv = (0 : dlzka / 2 - 1) / dlzka * Fs;
signal = abs(fft(s));
signal = signal(1 : dlzka / 2);
filtered_signal = abs(fft(filter(B, A, s)));
filtered_signal = filtered_signal(1 : dlzka / 2);
hold on
plot(frekv, signal);
plot(frekv, filtered_signal);
hold off 
xlabel('f [Hz]');

%9)
x = hist(s,50);
plot(x/dlzka);
suc = sum(x/dlzka); 

% suc == 1 -> integral je 1

%10)
koef = [-50:50];
r =[];
ri = 1;
for i = -50:50
    suma = 0;
    for c = 1:dlzka
        idx = 0;
        if ((c+i) >= 1 && (c+i) <= dlzka)
            idx = s(c+i);
        end
        suma = suma + s(c)*idx;
    end
    r(ri) = 1/dlzka* suma;
    ri = ri +1;
end
plot(koef,r);grid;

%11)
zero_r = find(koef == 0);
str = sprintf('Hodnota R[0] is %g', r(zero_r));
disp(str);

first_r = find(koef == 1);
str = sprintf('Hodnota R[1] is %g', r(first_r));
disp(str);

sixteen_r = find(koef == 16);
str = sprintf('Hodnota R[16] is %g', r(sixteen_r));
disp(str);

%12)
L = 50;
x = linspace(min(s), max(s), L);
h = zeros(L, L);
[~, ind1] = min(abs(repmat(s(:)', L, 1) - repmat(x(:), 1, dlzka)));
ind2 = ind1(1 + 1 : dlzka);
for i = 1 : dlzka - 1,
	d_f = ind1(i);
	d_s = ind2(i);
	h(d_f, d_s) = h(d_f, d_s) + 1;
end
surf = (x(2) - x(1)) ^ 2;
p = h / (dlzka - 1) / surf;
f = figure('Visible', 'off');
imagesc(x, x, p);
axis xy;
colorbar;
xlabel('x2');
ylabel('x1');
print(f, '-depsc', '12.eps');


%13)
check = sum(sum(p)) * surf;
fprintf('Overenie, æe sa jedn· o spr·vnu zdruæen˙ funkciu hustoty rozdelenia pravdepodobnosti, 2D integr·l by mal byª rovn˝ 1 a je rovn˝ %f.\n', check);

%14)
fprintf('Hodnota koeficientu R[1] je %f.\n', sum(sum(repmat(x(:), 1, L) .* repmat(x(:)', L, 1) .* p)) * surf);
