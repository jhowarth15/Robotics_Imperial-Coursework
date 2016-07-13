#!/usr/bin/env python
# By Jacek Zienkiewicz and Andrew Davison, Imperial College London, 2014
# Based on original C code by Adrien Angeli, 2009

import os
import math
import numpy as np
from sonarClass import Sonar
# import brickpi
import time
# from scipy.ndimage.filters import gaussian_filter

# Location signature class: stores a signature characterizing one location
class LocationSignature:
    def __init__(self, _no_bins = 300): #120
        self.no_bins = _no_bins
        self.sig = np.zeros(self.no_bins)# [0] * no_bins
        
    def print_signature(self):
        for i in range(len(self.sig)):
            print self.sig[i]

# --------------------- File management class ---------------
class SignatureContainer():
    maxError = 50
    def __init__(self, size = 20):
        self.size      = size; # max number of signatures that can be stored
        self.filenames = [];
        
        # Fills the filenames variable with names like loc_%%.dat 
        # where %% are 2 digits (00, 01, 02...) indicating the location number. 
        for i in range(self.size):
            self.filenames.append('loc_{0:02d}.dat'.format(i))

    # Get the index of a filename for the new signature. If all filenames are 
    # used, it returns -1;
    def get_free_index(self):
        n = 0
        while n < self.size:
            if (os.path.isfile(self.filenames[n]) == False):
                break
            n += 1
            
        if (n >= self.size):
            return -1;
        else:    
            return n;

    # Delete all loc_%%.dat files
    def delete_loc_files(self):
        print "STATUS:  All signature files removed."
        for n in range(self.size):
            if os.path.isfile(self.filenames[n]):
                os.remove(self.filenames[n])
            
    # Writes the signature to the file identified by index (e.g, if index is 1
    # it will be file loc_01.dat). If file already exists, it will be replaced.
    def save(self, signature, index):
        filename = self.filenames[index]
        if os.path.isfile(filename):
            os.remove(filename)
            
        f = open(filename, 'w')

        for i in range(len(signature.sig)):
            s = str(int(signature.sig[i])) + "\n"
            f.write(s)
        f.close();

    # Read signature file identified by index. If the file doesn't exist
    # it returns an empty signature.
    def read(self, index):
        ls = LocationSignature()
        filename = self.filenames[index]
        if os.path.isfile(filename):
            f = open(filename, 'r')
            for i in range(len(ls.sig)):
                s = f.readline()
                if (s != ''):
                    ls.sig[i] = int(s)
            f.close();
        else:
            print "WARNING: Signature does not exist."
        
        return ls
        
    # FILL IN: spin robot or sonar to capture a signature and store it in ls
    def characterize_location(self):
        result = self.getSignature()
        #print "TODO:    You should implement the function that captures a signature."
        # for i in range(len(ls.sig)):
        #     ls.sig[i] = result[i]
        return result

    # Convert depth vs. angle histogram to a depth frequency histogram
    def depth_histogram(self, ls):
        hist = [0] * 52
        
        for i in range(len(ls.sig)):
            j = ls.sig[i] // 5
            hist[int(j)] += 1
        # hist = np.histogram(ls.sig, bins=60, range=(0, 255))[0]
        # print hist
        return hist

    # calculate sum of square differences between two depth frequency histograms
    def square_diffs(self, depth1, depth2):
        sum = 0
        for i in range(len(depth1)):
            if (depth1[i]-depth2[i]<self.maxError):
                sum += math.pow(depth1[i]-depth2[i], 2)
            else:
                sum += self.maxError ** 2
        return sum



    # FILL IN: compare two signatures
    def compare_signatures(self, ls1, ls2):
        dist = 0
        # depth1 = guassian_blur(self.depth_histogram(ls1), sigma=2)
        # depth2 = guassian_blur(self.depth_histogram(ls2), sigma=2)
        depth1 = self.depth_histogram(ls1)
        depth2 = self.depth_histogram(ls2)
        #dist1 = self.square_diffs(depth1[:-1], depth2[:-1])
        dist2 = self.square_diffs(depth1, depth2)
        #dist3 = np.sum(abs(depth1 - depth2))
        
        # print "dist1: ", dist1, "dist2: ", dist2, "dist3:", dist3
        
        return dist2

    # This function characterizes the current location, and stores the obtained 
    # signature into the next available file.
    def learn_location(self, ls):
        # ls = LocationSignature(300)
        # self.characterize_location()
        idx = self.get_free_index();
        if (idx == -1): # run out of signature files
            print "\nWARNING:"
            print "No signature file is available. NOTHING NEW will be learned and stored."
            print "Please remove some loc_%%.dat files.\n"
            return

        self.save(ls,idx)
        print "STATUS:  Location " + str(idx) + " learned and saved."

    # This function tries to recognize the current location.
    # 1.   Characterize current location
    # 2.   For every learned locations
    # 2.1. Read signature of learned location from file
    # 2.2. Compare signature to signature coming from actual characterization
    # 3.   Retain the learned location whose minimum distance with
    #      actual characterization is the smallest.
    # 4.   Display the index of the recognized location on the screen
    
    """
    def recognize_location(self, ls_obs):        
        dist = [0] * self.size
        # FILL IN: COMPARE ls_read with ls_obs and find the best match
        for idx in range(self.size):
            # print "STATUS:  Comparing signature " + str(idx) + " with the observed signature."
            ls_read = self.read(idx)
            dist[idx] = self.compare_signatures(ls_obs, ls_read)
            
        est = np.zeros(5)
        for i in range(self.size):
            est[i % 5] += dist[i]
            
        
        return np.argmin(est)
    
    def recognize_angle(self, ls_obs, location_idx):
        err = np.zeros(ls_obs.no_bins)
        best_guess = np.zeros(4)
        # print "STATUS: Estimating angle"
        for j in range(4):
            ls_read = self.read(location_idx + (5 * j))
            for i in range(ls_obs.no_bins):    
                err[i] = np.sum(abs(np.roll(ls_obs.sig, -i) - ls_read.sig))            
            
            # print "Comparing file: {0}".format(location_idx + (5 * j)) 
            best_guess[j] = np.argmin(err)
        
        est_angle = 2.0 * ((np.mean(best_guess) / float(ls_obs.no_bins)) * math.pi)
        
        # print "STATUS: Best angle found. Offset: ", best_guess, ", Angle: ", est_angle, "Errors: ", err
        
        return est_angle
    """
    
    
    def recognize_location(self, ls_obs):        
        dist = [0] * self.size

        # FILL IN: COMPARE ls_read with ls_obs and find the best match
        for idx in range(self.size):
            print "STATUS:  Comparing signature " + str(idx) + " with the observed signature."
            ls_read = self.read(idx)
            dist[idx] = self.compare_signatures(ls_obs, ls_read)
        return np.argmin(dist) % 5
    
    def recognize_angle(self, ls_obs, location_idx):
        ls_read = self.read(location_idx)
        
        err = np.zeros(ls_obs.no_bins)
        terr = np.zeros(ls_obs.no_bins)
        print "STATUS: Estimating angle"
        for i in range(ls_obs.no_bins):
            terr = (np.roll(ls_obs.sig, -i) - ls_read.sig) ** 2
            terr[terr > self.maxError ** 2] = self.maxError ** 2
            err[i] = terr.sum()
            # err[i] = np.sum((np.roll(ls_obs.sig, -i) - ls_read.sig) ** 2)
            
        best_guess = np.argmin(err)
        
        est_angle = 2.0 * ((best_guess / float(ls_obs.no_bins)) * math.pi) # ((best_guess / float(ls_obs.no_bins)) * math.pi) - math.pi
        
        print "STATUS: Best angle found. Offset: ", best_guess, ", Angle: ", est_angle
        
        return est_angle
    
    def recognize_location_and_angle(self, ls_obs):         
        minDists = np.zeros(self.size)
        bestAngles = np.zeros(self.size)
        err = np.zeros(ls_obs.no_bins)
        
        for idx in range(self.size):
            # print "STATUS:  Comparing signature " + str(idx) + " with the observed signature."
            ls_read = self.read(idx)
            
            for i in range(ls_obs.no_bins):    
                # err[i] = np.sum((np.roll(ls_obs.sig, -i) - ls_read.sig) ** 2)            
                terr = (np.roll(ls_obs.sig, -i) - ls_read.sig) ** 2
                terr[terr > self.maxError ** 2] = self.maxError ** 2
                err[i] = terr.sum()
            
            best_guess = err.argmin() 
            minDists[idx] = err[best_guess]
            bestAngles[idx] = 2.0 * ((best_guess / float(ls_obs.no_bins)) * math.pi)
            
            # print "Best= ", best_guess, "MinDist", minDists[idx], "Best Angle", bestAngles[idx], "Err = ", err
        
        best_guess = minDists.argmin() % 5
                                            
        return best_guess, bestAngles[best_guess]
    