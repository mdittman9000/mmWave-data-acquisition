function val=test(a, b, c, d)
    fid = fopen( 'results.txt', 'wt' );
    a
    b
    c
    d
    fprintf( fid, '%f,%f,%f,%f\n', a,b,c,d);
    fclose(fid)
end