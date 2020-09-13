function[all_intervals] = calculate_intervals(distance_matrix, max_dimension, max_filtration_value, num_divisions, nu, name)

 %clc; clear all; close all;
 javaaddpath('./lib/javaplex.jar');
 import edu.stanford.math.plex4.*;
 javaaddpath('./lib/plex-viewer.jar');
 import edu.stanford.math.plex_viewer.*;
 cd './utility';
 addpath(pwd);
 cd '..';
 
 distances = distance_matrix + transpose(distance_matrix);
 m_space = metric.impl.ExplicitMetricSpace(distances);
 
 max_dimension = int16(max_dimension);
 max_filtration_value = single(max_filtration_value);
 num_divisions = int16(num_divisions);
 nu = int16(nu);
 
 for num_landmark_points = 50
     all_intervals = "";
     for i = 1:3
         maxmin_selector = api.Plex4.createMaxMinSelector(m_space, int16(num_landmark_points)); 
         %maxmin_selector =  api.Plex4.createRandomSelector(m_space, int16(num_landmark_points));

         stream = streams.impl.LazyWitnessStream(maxmin_selector.getUnderlyingMetricSpace(), maxmin_selector, max_dimension, max_filtration_value, nu, num_divisions);
         stream.finalizeStream();
         stream.getSize()
         persistence = api.Plex4.getModularSimplicialAlgorithm(max_dimension, 2);
         intervals = persistence.computeIntervals(stream);
         
         all_intervals = all_intervals + intervals.toString().toCharArray';
         
         options.filename = name + " " + string(num_landmark_points) + " v" + string(i);
         options.max_filtration_value = max_filtration_value;
         options.max_dimension = max_dimension-1;
         options.file_format = "png";
         plot = my_plot_barcodes(intervals, options);
     end
 end
end


