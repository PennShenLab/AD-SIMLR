clear
clc
close all

addpath('data')
addpath('src')

data_path = "data/Test_1_mECS.mat"; %% Insert the path to data in the quotes
output_folder = "results";

load(data_path);
% dataset = readtable(data_path); 

% data = dataset{:,2:end}; %% Remove indices
data = in_X;
X = normalize(data);

rng(95584,'twister'); %% For reproducibility

[S00, y_simlr, S_simlr, F_simlr, ydata_simlr,~,~,~,LF_simlr] = SIMLR(X,3,10); %% without graph diffusion
[S000, y_simlr_diff, S_simlr_diff, F_simlr_diff, ydata_simlr_diff, ~, ~,~,LF_simlr_diff] = SIMLRv2(X,3,10); %% with graph diffusion
S000(S000<0) = 0; %% These are entries -0.0000 and we need to make them non-negative

%% K-Means
y_kmeans = kmeans(X, 3);
ydata_kmeans = tsne(X);
sil_kmeans = mean(silhouette(X, y_kmeans));

%% Spectral Clustering
[y_spec, V_spec] = spectralcluster(S00,3,'Distance','precomputed');
ydata_spec = tsne(V_spec);
sil_SC = mean(silhouette(V_spec,y_spec));

%% Spectral Clustering with Graph Diffusion
[y_spec_diff, V_spec_diff] = spectralcluster(S000,3,'Distance','precomputed');
ydata_spec_diff = tsne(V_spec_diff);
sil_SC_diff = mean(silhouette(V_spec_diff,y_spec_diff));

%% SIMLR
sil_simlr = mean(silhouette(F_simlr, y_simlr));

%% SIMLR with Graph Diffusion
sil_simlr_diff = mean(silhouette(F_simlr_diff, y_simlr_diff));

%% Save Silhouette scores
silhouette_results = [sil_kmeans sil_SC sil_SC_diff sil_simlr sil_simlr_diff];
sil_table = array2table(silhouette_results);
sil_table.Properties.VariableNames(1:5) = {'kmeans','SC','SC_diff','SIMLR','SIMLR_diff'};
writetable(sil_table, output_folder+'/silhouette_scores.csv');

%% Save SC and SIMLR implementation results
writematrix(S00, output_folder+'/simMat_SC.txt')
writematrix(S_simlr, output_folder+'/simMat_simlr.txt')
writematrix(S000, output_folder+'/simMat_SC_diff.txt')
writematrix(S_simlr_diff, output_folder+'/simMat_simlr_diff.txt')
writematrix(y_kmeans, output_folder+'/clusters_labels_kmeans.txt')
writematrix(ydata_kmeans, output_folder+'/tsne_visualization_kmeans.txt')
writematrix(V_spec, output_folder+'/latent_SC.txt');
writematrix(y_spec, output_folder+'/clusters_labels_SC.txt')
writematrix(ydata_spec, output_folder+'/tsne_visualization_SC.txt')
writematrix(V_spec_diff, output_folder+'/latent_SC_diff.txt');
writematrix(y_spec_diff, output_folder+'/clusters_labels_SC_diff.txt')
writematrix(ydata_spec_diff, output_folder+'/tsne_visualization_SC_diff.txt')
writematrix(F_simlr, output_folder+'/latent_SIMLR.txt');
writematrix(y_simlr, output_folder+'/clusters_labels_SIMLR.txt')
writematrix(ydata_simlr, output_folder+'/tsne_visualization_SIMLR.txt')
writematrix(F_simlr_diff, output_folder+'/latent_SIMLR_diff.txt');
writematrix(y_simlr_diff, output_folder+'/clusters_labels_SIMLR_diff.txt')
writematrix(ydata_simlr_diff, output_folder+'/tsne_visualization_SIMLR_diff.txt')