import time
import sys
import psutil

class Sequence_Alignment_Efficient:

    def align_sequence(self,str_1,str_2):
        m = len(str_1)
        n = len(str_2)

        opt = [[0] * (n + 1) for i in range(m + 1)]

        alpha = {'AA': 0, 'CC': 0, 'GG': 0, 'TT': 0, 
                'AC': 110, 'CA': 110, 'AG': 48, 'GA': 48, 
                'AT': 94, 'TA': 94, 'CG': 118, 'GC': 118,
                'CT': 48, 'TC': 48, 'GT': 110, 'TG': 110}
        delta = 30

        for i in range(1, m + 1):
            opt[i][0] = i*delta
        for j in range(0, n + 1):
            opt[0][j] = j*delta

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                string = str_1[i - 1] + str_2[j - 1]
                opt[i][j] = min(opt[i - 1][j - 1] + alpha[string],
                               opt[i][j-1] + delta, opt[i-1][j] + delta)

        i, j = m, n
        x = ""
        y = ""

        while i and j:
            string = str_1[i - 1] + str_2[j - 1]
            if opt[i][j] == opt[i-1][j-1] + alpha[string]:
                x = str_1[i - 1] + x
                y = str_2[j - 1] + y
                i -= 1
                j -= 1
            elif opt[i][j] == opt[i - 1][j] + delta:
                x = str_1[i - 1] + x
                y = "_" + y
                i -= 1
            elif opt[i][j] == opt[i][j - 1] + delta:
                x = "_" + x
                y = str_2[j - 1] + y
                j -= 1

        while i:
            x = str_1[i - 1] + x
            y = "_" + y
            i -= 1

        while j:
            x = "_" + x
            y = str_2[j - 1] + y
            j -= 1

        return x, y, opt[m][n]


    def div_and_conquer_sol(self, str_1, str_2):
        m = len(str_1)
        n = len(str_2)
        if m < 2 or n < 2:
            return self.align_sequence(str_1, str_2)
        else:
            left_part = self.align_space_efficient(str_1[:m // 2], str_2, 0)
            right_part = self.align_space_efficient(str_1[m // 2:], str_2, 1)
            
            new_list = [left_part[j] + right_part[n - j] for j in range(n + 1)]
            
            min_index = new_list.index(min(new_list))
            
            left_call = self.div_and_conquer_sol(str_1[:len(str_1) // 2], str_2[:min_index])
            right_call = self.div_and_conquer_sol(str_1[len(str_1) // 2:], str_2[min_index:])
            
            l = [left_call[r] + right_call[r] for r in range(3)]
            
        return [left_call[r] + right_call[r] for r in range(3)]


    def align_space_efficient(self, X, Y, flag):
        m = len(X)
        n = len(Y)

        opt = []

        alpha = {'AA': 0, 'CC': 0, 'GG': 0, 'TT': 0, 
                 'AC': 110, 'CA': 110, 'AG': 48, 'GA': 48, 
                 'AT': 94, 'TA': 94, 'CG': 118, 'GC': 118, 
                 'CT': 48, 'TC': 48, 'GT': 110, 'TG': 110}
        delta = 30

        for i in range(m + 1):
            opt.append([0] * (n + 1))
        for j in range(n + 1):
            opt[0][j] = j*delta
        
        if flag == 0:
            for i in range(1, m + 1):
                opt[i][0] = opt[i - 1][0] + delta
                for j in range(1, n + 1):
                    opt[i][j] = min(opt[i - 1][j - 1] + alpha[X[i - 1] + Y[j - 1]],
                                   opt[i][j - 1] + delta,
                                   opt[i - 1][j] + delta)
                opt[i - 1] = []
        elif flag == 1:
            for i in range(1, m + 1):
                opt[i][0] = opt[i - 1][0] + delta
                for j in range(1, n + 1):
                    opt[i][j] = min(opt[i - 1][j - 1] + alpha[X[m - i] + Y[n - j]],
                                   opt[i][j - 1] + delta,
                                   opt[i - 1][j] + delta)
                opt[i - 1] = []
        return opt[m]


    def generate_string(self, s, index_list):
        string_list = list(s)
        for i in index_list:
            string_list = string_list[0:i + 1] + string_list + string_list[i + 1:]
        return "".join(string_list)


def memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    return int(memory_info.rss/1024)

def efficient_implementation(in_file_loc,out_file_loc):
    f = open(in_file_loc, 'r')

    chars_1 = f.readline()
    while (chars_1[-1] in ['\n', '\r']):
        chars_1 = chars_1[:-1]
    
    nums = f.readline()
    while (nums[-1] in ['\n', '\r']):
        nums = nums[:-1]

    index1 = []
    while nums.isnumeric():
        index1.append(int(nums))
        nums = f.readline()
        while nums[-1] in ['\n', '\r']:
            nums = nums[:-1]

    chars_2 = nums
    nums = f.readline()
    while (nums[-1] in ['\n', '\r']):
        nums = nums[:-1]

    index2 = []
    while len(nums)!=0:
        index2.append(int(nums))
        nums = f.readline()
        
    f.close()

    res = Sequence_Alignment_Efficient()
    str_1 = res.generate_string(chars_1, index1)
    str_2 = res.generate_string(chars_2, index2)
    start = time.time()
    results = res.div_and_conquer_sol(str_1, str_2)
    total_memory = memory()
    end = time.time()
    total_time = (end - start)*1000
    
    f = open(out_file_loc, 'w')
    f.write(str(int(results[2])) + "\n\n")
    f.write(results[0][:] + "\n\n")
    f.write(results[1][:] + "\n\n")
    f.write(str(float("{:.4f}".format(total_time))) + "\n\n")
    f.write(str(float(total_memory)))
    f.close()

    param_list = [total_memory, float("%.4f"%total_time), len(str_1)+len(str_2)]
    
    return param_list

if __name__ == "__main__":
    param_list = efficient_implementation(sys.argv[-2],sys.argv[-1])



