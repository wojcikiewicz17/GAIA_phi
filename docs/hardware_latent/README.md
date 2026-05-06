# Hardware Latent (Bare-Metal) — Matriz Técnica Auditável

> Escopo: documentação técnica verificável de técnicas bare-metal **sem integração no build principal**.
>
> Restrições desta etapa: sem alterações em CMake, sem alterações em `gaia_core_v2`, `gaia_engines_v2`, `llama_guard`, sem integração Magisk, sem integração llama, sem criação de módulo compilável.

## Categorias

- **Fato de datasheet**: comportamento especificado por documentação oficial de MCU/SoC.
- **Técnica aplicável**: uso prático consolidado em firmware/sistemas embarcados.
- **Hipótese experimental**: caminho plausível, porém dependente de validação em ambiente-alvo.
- **Benchmark pendente**: otimização conhecida sem afirmação de ganho até medição reprodutível.

## Matriz técnica (12 técnicas iniciais)

| ID | plataforma | técnica | registradores envolvidos | efeito esperado | dependência de hardware | método de validação | risco | status |
|---|---|---|---|---|---|---|---|---|
| HL-001 | AVR (ATmega328P classe) | AVR GPIO toggle via PINB | `DDRB`, `PORTB`, `PINB` | Toggle de pino com baixa latência por escrita em `PINB` | MCU AVR com semântica de toggle por escrita em registro PIN | Osciloscópio/analisador lógico comparando período de toggle vs rotina `digitalWrite`/equivalente | Escrita indevida em máscara pode afetar múltiplos bits | verificado |
| HL-002 | AVR (16-bit timer) | AVR Timer1 CTC | `TCCR1A`, `TCCR1B`, `OCR1A`, `TIMSK1`, `TCNT1` | Base temporal precisa por compare match em modo CTC | Timer1 disponível e clock/prescaler estável | Medir jitter e período de interrupção em pino de debug/contador de eventos | Configuração errada de prescaler/OCR1A gera deriva temporal | verificado |
| HL-003 | AVR (PWM HW) | AVR PWM 10-bit | `TCCR1A`, `TCCR1B`, `OCR1A/OCR1B`, `ICR1` (modo dependente) | PWM de maior resolução para controle fino de duty cycle | Canal PWM 16-bit com modo 10-bit habilitável | Medir duty efetivo e frequência em diferentes cargas | Ruído/aliasing em carga real e escolha incorreta de modo PWM | documentado |
| HL-004 | AVR (USART) | AVR UART polling | `UCSR0A`, `UCSR0B`, `UCSR0C`, `UBRR0`, `UDR0` | TX/RX sem ISR via polling de flags | UART integrada e baud compatível com clock | Loopback serial e teste de framing/error flags em múltiplas taxas | Bloqueio de CPU e perda de bytes sob carga | verificado |
| HL-005 | AVR (SPI) | AVR SPI master | `SPCR`, `SPSR`, `SPDR`, `DDRB`, `PORTB` (SS/MOSI/MISO/SCK) | Comunicação síncrona master com periféricos SPI | Barramento SPI elétrico estável e níveis lógicos compatíveis | Transferências padrão (JEDEC ID/registro conhecido) com checagem de integridade | Conflito de CS/timing e perda por clock inadequado | verificado |
| HL-006 | AVR (ADC) | AVR ADC free-running | `ADMUX`, `ADCSRA`, `ADCSRB`, `ADCH/ADCL`, `DIDR0` | Amostragem contínua com menor overhead por conversão automática | ADC interno e referência analógica estável | Capturar taxa efetiva e variância do ruído por janela de amostras | Acoplamento de ruído de alimentação e erro de referência | documentado |
| HL-007 | AVR (Power/Reset) | AVR watchdog wake | `WDTCSR`, `MCUSR`, modo sleep (`SMCR`) | Acordar MCU periodicamente com consumo reduzido | Watchdog funcional em sleep mode e reset flags confiáveis | Medir corrente média e periodicidade de wake | Reset inesperado por sequência incorreta de configuração | documentado |
| HL-008 | AVR (NVM) | AVR EEPROM read/write | `EEAR`, `EEDR`, `EECR` | Persistência de configuração fora de energia | EEPROM interna com endurance limitada | Teste de escrita/leitura/verificação CRC e ciclo de retenção | Desgaste por escrita frequente sem wear leveling | verificado |
| HL-009 | Raspberry Pi (Linux userspace) | Raspberry Pi GPIO via mmap | Mapeamento de `GPFSEL*`, `GPSET*`, `GPCLR*`, `GPLEV*` | Controle GPIO de baixa sobrecarga em userspace | SoC Broadcom compatível + permissões `/dev/mem` ou interface equivalente | Medir latência de toggle com analisador lógico comparando sysfs/libgpiod | Fragilidade por mudanças de base address/permissions entre modelos | hipótese |
| HL-010 | Raspberry Pi (SoC timer) | Raspberry Pi system timer | Registradores do system timer (`CLO/CHI` e compare) | Timestamp de alta resolução e agendamento de eventos | Disponibilidade/estabilidade do timer do SoC no modelo alvo | Comparar monotonicidade e resolução contra `clock_gettime` | Diferenças entre gerações de SoC e interferência do scheduler | documentado |
| HL-011 | ARM64 (AArch64) | ARM64 cycle counter | `PMCCNTR_EL0`, `PMCR_EL0`, `PMCNTENSET_EL0` (acesso condicionado) | Contagem de ciclos para microbench e profiling fino | Kernel/EL0 deve permitir acesso aos PMU counters | Medir ciclos de rotinas fixas com repetição e estatística de dispersão | Acesso bloqueado por política do kernel ou virtualização | pendente de bench |
| HL-012 | ARM64 (AArch64 SIMD) | ARM64 NEON vector path | Registradores vetoriais `V0..V31` (NEON/ASIMD) | Aceleração vetorial de operações paralelas | CPU com suporte NEON e alinhamento/memória adequados | Benchmark A/B escalar vs vetorial com mesmo dataset | Regressão por bandwidth/cache e auto-vectorização inconsistente | pendente de bench |

---

## Detalhamento por técnica

### HL-001 — AVR GPIO toggle via PINB
- **Descrição curta:** toggle direto de saída em AVR escrevendo máscara no registro `PINB`.
- **Por que é latente:** evita camadas de abstração e reduz overhead de instruções.
- **Como validar:** medir frequência máxima de comutação e jitter em pino dedicado.
- **O que não afirmar sem medição:** “X vezes mais rápido” em relação a APIs de alto nível.

### HL-002 — AVR Timer1 CTC
- **Descrição curta:** geração de base de tempo por compare match no Timer1 em modo CTC.
- **Por que é latente:** temporização determinística com baixo custo de CPU.
- **Como validar:** medir período real e jitter por interrupção em janela longa.
- **O que não afirmar sem medição:** precisão absoluta sob qualquer configuração de clock.

### HL-003 — AVR PWM 10-bit
- **Descrição curta:** uso de modo PWM 10-bit em timer de 16 bits.
- **Por que é latente:** aumenta granularidade de duty cycle sem processamento adicional.
- **Como validar:** varrer duty e medir linearidade/frequência em carga real.
- **O que não afirmar sem medição:** melhoria perceptível de controle em todos os atuadores.

### HL-004 — AVR UART polling
- **Descrição curta:** transmissão/recepção UART por polling de flags de status.
- **Por que é latente:** remove latência/interferência de ISR em cenários simples.
- **Como validar:** loopback com diferentes baud rates e análise de erros.
- **O que não afirmar sem medição:** robustez sob tráfego alto concorrente.

### HL-005 — AVR SPI master
- **Descrição curta:** operação SPI master por acesso direto a registradores.
- **Por que é latente:** minimiza overhead de driver genérico em transações curtas.
- **Como validar:** leitura/escrita de registradores conhecidos em periférico SPI.
- **O que não afirmar sem medição:** throughput sustentado máximo em qualquer topologia.

### HL-006 — AVR ADC free-running
- **Descrição curta:** ADC em conversão contínua automática.
- **Por que é latente:** maximiza taxa de amostragem útil com menor intervenção da CPU.
- **Como validar:** medir SPS efetivo, ruído RMS e estabilidade da referência.
- **O que não afirmar sem medição:** precisão metrológica em ambiente ruidoso.

### HL-007 — AVR watchdog wake
- **Descrição curta:** watchdog para despertar periódico em modos de baixo consumo.
- **Por que é latente:** habilita duty cycling energético com firmware enxuto.
- **Como validar:** medir corrente média e intervalo de wake ao longo do tempo.
- **O que não afirmar sem medição:** consumo “ultrabaixo” universal sem perfil de carga.

### HL-008 — AVR EEPROM read/write
- **Descrição curta:** persistência de parâmetros via EEPROM interna.
- **Por que é latente:** armazenamento não volátil sem componentes externos.
- **Como validar:** testes de integridade (CRC), retenção e ciclos de escrita.
- **O que não afirmar sem medição:** vida útil elevada sem estratégia de desgaste.

### HL-009 — Raspberry Pi GPIO via mmap
- **Descrição curta:** acesso direto aos registradores GPIO mapeados em memória.
- **Por que é latente:** reduz overhead de pilhas de software de I/O.
- **Como validar:** medir latência de borda e estabilidade temporal em carga do sistema.
- **O que não afirmar sem medição:** determinismo hard real-time em Linux userspace.

### HL-010 — Raspberry Pi system timer
- **Descrição curta:** uso do timer de sistema do SoC para marcação temporal fina.
- **Por que é latente:** oferece referência temporal direta independente de APIs de alto nível.
- **Como validar:** comparar resolução e drift contra relógio monotônico do kernel.
- **O que não afirmar sem medição:** superioridade consistente em todos os modelos Raspberry Pi.

### HL-011 — ARM64 cycle counter
- **Descrição curta:** leitura de contador de ciclos da PMU para microbench.
- **Por que é latente:** observabilidade de custo por trecho de código em granularidade de ciclo.
- **Como validar:** repetir medições com isolamento de afinidade e estatística robusta.
- **O que não afirmar sem medição:** ganhos absolutos de otimização sem intervalo de confiança.

### HL-012 — ARM64 NEON vector path
- **Descrição curta:** caminho vetorial NEON para processamento paralelo de dados.
- **Por que é latente:** explora largura SIMD subutilizada em caminhos escalares.
- **Como validar:** benchmark A/B com datasets e alinhamento controlados.
- **O que não afirmar sem medição:** aceleração fixa (ex.: “4x”) em qualquer workload.

## Técnicas prometidas mas ainda não consolidadas

- CAN bus software sem MCP2515
- ADC sigma-delta virtual
- DMA simulado via SPI/Timer
- osciloscópio com Arduino
- BNN em AVR
- processamento de imagem NEON sem OpenCV

> Status desta seção: **hipótese/roadmap técnico**, sem consolidação experimental nesta etapa.

## Conformidade desta entrega

- Sem código executável novo.
- Sem módulo compilável novo.
- Sem integração no build principal.
- Sem alteração de CMake.
- Sem alteração em `gaia_core_v2`, `gaia_engines_v2`, `llama_guard`.
