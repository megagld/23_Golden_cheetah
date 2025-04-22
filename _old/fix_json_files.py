import os
import pymsgbox

# usuwa z plików json Rouvy ostatnią linię

def main():
        
    def fix_file(file_path):
        data = open(file_path).read().splitlines()
        with open(file_path, "w") as fh:
            fh.write(f"{data[0]}")   

    input_dir = os.getcwd()

    cnt=0

    for i,_,k in os.walk(input_dir):
        for l in k:
            if l.endswith('.json'):
                    file_path='{}\\{}'.format(i,l)
                    fix_file(file_path)
                    cnt+=1
                    
    pymsgbox.alert(text=f'Naprawione pliki .json :{cnt}szt.')

if __name__ == "__main__":
    main()
