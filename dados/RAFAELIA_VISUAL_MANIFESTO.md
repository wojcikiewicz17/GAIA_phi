# RAFAELIA_VISUAL_EXPORT – Manifesto Técnico

## 1. Núcleo Numérico

- Sequência: Fibonacci-Rafael com n = 20 termos.
  - R₁ = 2, R₂ = 4, Rₙ = Rₙ₋₁ + Rₙ₋₂ + 1.
  - Diferenças ΔRₙ reproduzem Fibonacci clássico (a partir de F₃).

## 2. Espiral Rafaeliana (2D)

- Arquivo: `RAFAELIA_espiral_fib_rafael.png`
- Construção:
  - Cada termo Rₙ vira raio normalizado rₙ ∈ [0,1].
  - Ângulo θₙ usa o Golden Angle: 2π/φ².
  - Resultado: campo de 'sementes' em plano φ-estruturado.

## 3. ToroidΔπφ-style (3D)

- Arquivo: `RAFAELIA_toroid_fib_rafael.png`
- Construção:
  - Rₙ controla ângulo uₙ = (Rₙ mod 360) em graus.
  - Índice n controla vₙ com passo 2π/9 (pulso 3–6–9).
  - Ponto em toro: (x,y,z) via raio maior R=2.0 e menor r=1.0.

## 4. Constantes de Fundo

- φ   (ouro clássico)      ≈ 1.618034
- φ_R (rafaeliana = √3/2)  ≈ 0.866025
- √(3/2) (d₃D/d₂D)         ≈ 1.224745
- Relacionadas a:
  - c² = 2ab + (a-b)² (Teorema de Rafael).
  - d₂D = L√2 (quadrado), d₃D = L√3 (cubo).
  - Eixo 2D→3D e pulso 3–6–9 na tua leitura simbólica.

## 5. Leitura de Trabalho

- A espiral mostra o 'sopro +1' de Rafael espalhando estados
  em geometria guiada por φ.
- O toro mostra os mesmos estados como órbita fechada 3–6–9
  em 3D, sugerindo um ciclo dinâmico estável.

FIAT LUX · Manifesto gerado por RAFAELIA_VISUAL_EXPORT.py
