import sys
import os
import time

from imap_engine import EngineIMAP

class Demo(object):
    '''
    A very simple demo.
    '''
    def __init__(self, input_file) -> None:
        self.input_file = input_file
        self.engine = EngineIMAP(input_file, input_file+'.seq')

    def _opt_size(self):
        self.engine.rewrite()
        self.engine.add_sequence('rewrite')
        self.engine.refactor(zero_gain=True)
        self.engine.add_sequence('refactor -z')

    def _opt_depth(self):
        self.engine.balance()
        # self.engine.add_sequence('balance')

    def _opt_lut(self):
        self.engine.lut_opt()
        # self.engine.add_sequence('lut_opt')
    
    def _opt_ref(self):
        self.engine.refactor()
        # self.engine.add_sequence('refactor')
    
    def _opt_rew(self):
        self.engine.rewrite()
        # self.engine.add_sequence('rewrite')
    
    def sequence(self, list):
        for i in list:
            if i == 0:
                self.engine.add_sequence('rewrite')
            elif i == 1:
                self.engine.add_sequence('balance')
            elif i == 2:
                self.engine.add_sequence('refactor')
            else:
                self.engine.add_sequence('lut_opt')
        self.engine.add_sequence('map_fpga')
        self.engine.write()
    
    def _opt_who(self, who):
        if who == 0:
            self._opt_rew()
        elif who == 1:
            self._opt_depth()
        elif who == 2:
            self._opt_ref()
        else:
            self._opt_lut()
    
    def history_a(self):
        self.engine.history(add=True)
    
    def history_s(self):
        self.engine.history(size=True)

    def history_to(self):
        self.engine.history(backup=0)
    
    def history_c(self):
        self.engine.history(clear=True)

    def get_ele(self):
        f = open('/home/zephyr/Desktop/iMAP/stats_aig.txt','r')
        lines = f.readlines()
        area = int(lines[0])
        depth = int(lines[1])
        return([area,depth])

        


    # def run(self):
    #     self.engine.read()
    #     opt_round = 5
    #     while opt_round > 0:
    #         self._opt_size()
    #         self._opt_depth()
    #         self.engine.print_stats()
    #         opt_round -= 1

    #     self.engine.map_fpga()
    #     self.engine.add_sequence('map_fpga')
    #     self.engine.print_stats(type=1)
    
    def first_run(self):
        opt_num = [0,1,2,3]
        seq = []
        ele = []
        for i in opt_num:
            opt_num1 = opt_num[:i] + opt_num[i+1:]
            for j in range(3):
                opt_num2 = opt_num1[:j] + opt_num1[j+1:]
                j0 = opt_num1[j]
                for k in opt_num2:
                    t = opt_num2[0] if k == opt_num2[1] else opt_num2[1]
                    seq.append([i,j0,k,t])
                    index = i * 6 + j0 * 2 + k
                    self.engine.read()
                    self._opt_who(i)
                    self._opt_who(j0)
                    self._opt_who(k)
                    self._opt_who(t)
                    self.engine.map_fpga()
                    # self.engine.add_sequence('map_fpga')
                    # self.engine.add_sequence('\n')
                    self.engine.print_stats(type=1)
                    ele.append(self.get_ele())

        area = [el[0] for el in ele]
        depth = [el[1] for el in ele]
        area_ave = float(sum(area)) / float(len(area))
        depth_ave = sum(depth) / len(depth)
        area_1 = [a/area_ave for a in area]
        depth_1 = [d/depth_ave for d in depth]
        reward = [a*0.4 + d*0.6 for a, d in zip(area_1,depth_1)]
        reward_min = min(reward)
        index = reward.index(reward_min)
        print(ele)


        
        # self.engine.map_fpga()
        # self.engine.add_sequence('map_fpga')
        # self.engine.print_stats(type=1)
        # self.engine.print()
        # self.history_s()

        self.engine.write()
        return(seq[index])
    
    def first_run5(self):
        opt_num = [0,1,2,3]
        seq = []
        ele = []
        for i in opt_num:
            for j in opt_num:
                for k in opt_num:
                    for t in opt_num:
                        for m in opt_num:
                            seq.append([i,j,k,t,m])
                            index = i * 256 + j * 64 + k * 16 + t * 4 + m
                            self.engine.read()
                            self._opt_who(i)
                            self._opt_who(j)
                            self._opt_who(k)
                            self._opt_who(t)
                            self._opt_who(m)
                            self.engine.map_fpga()
                            # self.engine.add_sequence('map_fpga')
                            # self.engine.add_sequence('\n')
                            self.engine.print_stats(type=1)
                            ele.append(self.get_ele())
        area = [el[0] for el in ele]
        depth = [el[1] for el in ele]
        area_ave = sum(area) / len(area)
        depth_ave = sum(depth) / len(depth)
        area_1 = [a/area_ave for a in area]
        depth_1 = [d/depth_ave for d in depth]
        reward = [a*0.4 + d*0.6 for a, d in zip(area_1,depth_1)]
        reward_min = min(reward)
        index = reward.index(reward_min)
        print(reward_min,area[index],depth[index])
        return(seq[index],area_ave,depth_ave)
    
    def first_run4(self):
        opt_num = [0,1,2,3]
        seq = []
        ele = []
        for i in opt_num:
            for j in opt_num:
                for k in opt_num:
                    for t in opt_num:
                        seq.append([i,j,k,t])
                        index = i * 64 + j * 16 + k * 4 + t
                        self.engine.read()
                        self._opt_who(i)
                        self._opt_who(j)
                        self._opt_who(k)
                        self._opt_who(t)
                        self.engine.map_fpga()
                        # self.engine.add_sequence('map_fpga')
                        # self.engine.add_sequence('\n')
                        self.engine.print_stats(type=1)
                        ele.append(self.get_ele())
        area = [el[0] for el in ele]
        depth = [el[1] for el in ele]
        area_ave = sum(area) / len(area)
        depth_ave = sum(depth) / len(depth)
        area_1 = [a/area_ave for a in area]
        depth_1 = [d/depth_ave for d in depth]
        reward = [a*0.4 + d*0.6 for a, d in zip(area_1,depth_1)]
        reward_min = min(reward)
        index = reward.index(reward_min)
        print(reward_min,area[index],depth[index])
        return(seq[index],area_ave,depth_ave,reward_min,area[index],depth[index])
    
    def first_run3(self):
        opt_num = [0,1,2,3]
        seq = []
        ele = []
        for i in opt_num:
            for j in opt_num:
                for k in opt_num:
                    seq.append([i,j,k])
                    index = i * 16 + j * 4 + k
                    self.engine.read()
                    self._opt_who(i)
                    self._opt_who(j)
                    self._opt_who(k)
                    self.engine.map_fpga()
                    # self.engine.add_sequence('map_fpga')
                    # self.engine.add_sequence('\n')
                    self.engine.print_stats(type=1)
                    ele.append(self.get_ele())
        area = [el[0] for el in ele]
        depth = [el[1] for el in ele]
        area_ave = sum(area) / len(area)
        depth_ave = sum(depth) / len(depth)
        area_1 = [a/area_ave for a in area]
        depth_1 = [d/depth_ave for d in depth]
        reward = [a*0.4 + d*0.6 for a, d in zip(area_1,depth_1)]
        reward_min = min(reward)
        index = reward.index(reward_min)
        print(reward_min,area[index],depth[index])
        return(seq[index],area_ave,depth_ave,reward_min)
    
    def more_run(self, seq_cur):
        self.engine.read()
        for i in seq_cur:
            self._opt_who(i)
        self.history_a()
        opt_num = [0,1,2,3]
        seq = []
        ele = []
        for i in opt_num:
            opt_num1 = opt_num[:i] + opt_num[i+1:]
            for j in range(3):
                opt_num2 = opt_num1[:j] + opt_num1[j+1:]
                j0 = opt_num1[j]
                for k in opt_num2:
                    t = opt_num2[0] if k == opt_num2[1] else opt_num2[1]
                    seq.append([i,j0,k,t])
                    index = i * 6 + j0 * 2 + k
                    self.history_to()
                    self._opt_who(i)
                    self._opt_who(j0)
                    self._opt_who(k)
                    self._opt_who(t)
                    self.engine.map_fpga()
                    # self.engine.add_sequence('map_fpga')
                    # self.engine.add_sequence('\n')
                    self.engine.print_stats(type=1)
                    ele.append(self.get_ele())
        self.history_c()
        area = [el[0] for el in ele]
        depth = [el[1] for el in ele]
        area_ave = sum(area) / len(area)
        depth_ave = sum(depth) / len(depth)
        area_1 = [a/area_ave for a in area]
        depth_1 = [d/depth_ave for d in depth]
        reward = [a*0.4 + d*0.6 for a, d in zip(area_1,depth_1)]
        reward_min = min(reward)
        index = reward.index(reward_min)
        print(reward_min)
        return(seq[index])
    
    def less_run(self, seq_cur, area_ave, depth_ave):
        self.engine.read()
        for i in seq_cur:
            self._opt_who(i)
        self.history_a()
        opt_num = [0,1,2,3]
        seq = []
        ele = []
        for i in opt_num:
            for j in opt_num:
                for k in opt_num:
                    seq.append([i,j,k])
                    index = i * 16 + j * 4 + k
                    self.history_to()
                    self._opt_who(i)
                    self._opt_who(j)
                    self._opt_who(k)
                    self.engine.map_fpga()
                    # self.engine.add_sequence('map_fpga')
                    # self.engine.add_sequence('\n')
                    self.engine.print_stats(type=1)
                    ele.append(self.get_ele())
        self.history_c()
        area = [el[0] for el in ele]
        depth = [el[1] for el in ele]
        # area_ave = sum(area) / len(area)
        # depth_ave = sum(depth) / len(depth)
        area_1 = [a/area_ave for a in area]
        depth_1 = [d/depth_ave for d in depth]
        reward = [a*0.4 + d*0.6 for a, d in zip(area_1,depth_1)]
        reward_min = min(reward)
        index = reward.index(reward_min)
        print(reward_min,area[index],depth[index])
        return(seq[index],reward_min,area[index],depth[index])



# class HistoryDemo(Demo):
#     '''
#     A demo with history and choice mapping.
#     '''
#     def __init__(self, input_file, output_file) -> None:
#         super().__init__(input_file, output_file)

#     def _history_empty(self):
#         return self.engine.history(size=True) == 0

#     def _history_full(self):
#         return self.engine.history(size=True) == 5

#     def _history_add(self):
#         self.engine.history(add=True)
#         self.engine.add_sequence('history -a')

#     def _history_replace(self, idx):
#         self.engine.history(replace=idx)
#         self.engine.add_sequence(f'history -r {idx}')

#     def run(self):
#         self.engine.read()
#         opt_round = 10
#         current_size  = self.engine.get_aig_size()
#         current_depth = self.engine.get_aig_depth()
#         while opt_round > 0:
#             self._opt_size()
#             self._opt_lut()
#             self._opt_depth()
#             size = self.engine.get_aig_size()
#             depth = self.engine.get_aig_depth()
#             if depth < current_depth:
#                 if self._history_full():
#                     self._history_replace(-1)
#                 else:
#                     self._history_add()
#             elif depth == current_depth and size < current_size:
#                 if self._history_empty():
#                     self._history_add()

#             current_size = size
#             current_depth = depth
#             opt_round -= 1

#         self.engine.map_fpga(type=1)
#         self.engine.add_sequence('map_fpga')

#         self.engine.write()


# if __name__ == '__main__':
#     time1 = time.time()
    
    
#     # the way of read files one
#     d = Demo(sys.argv[1])
    
    
#     # the way of read files two


#     # d = HistoryDemo(sys.argv[1:])
#     out_first = d.first_run4()
#     seq_first = out_first[0]
#     area_ave = out_first[1]
#     depth_ave = out_first[2]
#     reward_min = out_first[3]
#     area_min = out_first[4]
#     depth_min = out_first[5]
#     for i in range(100):
#         out_second = d.less_run(seq_first,area_ave,depth_ave)
#         seq_second = out_second[0]
#         reward_1 = out_second[1]
#         area_1 = out_second[2]
#         depth_1 = out_second[3]
#         if reward_1 < reward_min:
#             seq_first += seq_second
#             reward_min = reward_1
#             area_min = area_1
#             depth_min = depth_1
#         else:
#             break

#     # seq_second = d.less_run(seq_first,area_ave,depth_ave)
#     # seq_third = d.less_run(seq_first+seq_second,area_ave,depth_ave)
#     print(seq_first,area_min,depth_min)
#     d.sequence(seq_first)
#     time2 =time.time()
#     print(time2 - time1)


if __name__ == '__main__':

    f = open('/home/zephyr/Desktop/iMAP/file_names.txt','r')
    lines = f.readlines()
    for line in lines:
        line = line.replace('\n','')
        path = '/home/zephyr/Desktop/iMAP/benchmark_eda_elite/' + line +'/' + line + '.aig'
        time1 = time.time()
        # the way of read files two
        d = Demo(path)

        # d = HistoryDemo(sys.argv[1:])
        out_first = d.first_run4()
        seq_first = out_first[0]
        area_ave = out_first[1]
        depth_ave = out_first[2]
        reward_min = out_first[3]
        area_min = out_first[4]
        depth_min = out_first[5]
        for i in range(100):
            out_second = d.less_run(seq_first,area_ave,depth_ave)
            seq_second = out_second[0]
            reward_1 = out_second[1]
            area_1 = out_second[2]
            depth_1 = out_second[3]
            if reward_1 < reward_min:
                seq_first += seq_second
                reward_min = reward_1
                area_min = area_1
                depth_min = depth_1
            else:
                break

        # seq_second = d.less_run(seq_first,area_ave,depth_ave)
        # seq_third = d.less_run(seq_first+seq_second,area_ave,depth_ave)
        print(seq_first,area_min,depth_min)
        d.sequence(seq_first)
        time2 =time.time()
        print(time2 - time1)

        path1 = '/home/zephyr/Desktop/iMAP/benchmark_eda_elite/' + line + '/output.txt'
        f1 = open(path1,'w')
        f1.write('area:' + str(area_min) + '\n')
        f1.write('depth:' + str(depth_min) + '\n')
        f1.write('time:' + str(time2 - time1) + '\n')
        f1.close()

    



