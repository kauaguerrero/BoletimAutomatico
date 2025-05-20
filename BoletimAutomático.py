from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


from time import sleep

login = str(input('Digite o login do academico: '))
senha = str(input('Digite a senha do acadêmico: '))

driver = webdriver.Chrome()
driver.get('https://academico.feituverava.com.br/index.php?class=LoginForm')
sleep(2)

# Faz o login
campo_login = driver.find_element(By.XPATH, "//input[@placeholder='Usuário']")
campo_login.send_keys(login)
campo_senha = driver.find_element(By.XPATH, "//input[@placeholder='Senha']")
campo_senha.send_keys(senha)

escolha_tipo = Select(driver.find_element(By.XPATH, "//select[@name='perfil']"))
escolha_tipo.select_by_visible_text("Aluno")  # ou "Professor"
sleep(3)

botao_entrar = driver.find_element(By.XPATH, "//button[@id='tbutton_btn_entrar']")
botao_entrar.click()

sleep(5)
botao_aluno = driver.find_element(By.XPATH, "//*[@id='side-menu']/li[1]/a")
botao_aluno.click()
sleep(2)

botao_boletim = driver.find_element(By.XPATH, "//*[@id='side-menu']/li[1]/ul/li[4]/a/span")
botao_boletim.click()
sleep(2)

ver_boletim = driver.find_element(
            By.CSS_SELECTOR,
            "a[href*='BoletimNovoList'] span.btn-default"  # [href*] = contém no href
        )
ver_boletim.click()
sleep(4)

tabela = driver.find_element(By.XPATH, "//table[contains(@class,'table') or contains(@id,'datagrid')]")
linhas = tabela.find_elements(By.XPATH, ".//tbody/tr[td]")

# Configurações de formatação
TAM_MATERIA = 40
TAM_NOTA = 15
TAM_FREQUENCIA = 10

print("\n=== BOLETIM ACADÊMICO ===")
print("=" * (TAM_MATERIA + TAM_NOTA + TAM_FREQUENCIA + 30))

for linha in linhas:
    cols = linha.find_elements(By.TAG_NAME, "td")
    if len(cols) >= 3:
        # Extrai e limpa os dados
        materia = cols[1].text.strip() or "N/A"
        nota = cols[2].text.strip() or "N/A"
        frequencia = cols[6].text.strip().replace('%', '') if cols[6].text.strip() else "0"

        try:
            # Verifica se é numérico antes de converter
            freq_num = float(frequencia) if frequencia.replace('.', '', 1).isdigit() else 0
            status = "✓ Aprovado" if freq_num >= 75.0 else "✗ Reprovado"
        except ValueError:
            status = "? Dado inválido"
            freq_num = 0

        # Formata a saída
        print(f"Matéria: {materia.ljust(TAM_MATERIA)[:TAM_MATERIA]} | Nota: {nota.center(TAM_NOTA)} | Freq: {str(freq_num).rjust(TAM_FREQUENCIA)}% {status}")
