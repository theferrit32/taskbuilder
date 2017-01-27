



char **get_lines(char *filename)
{
    FILE *fp = fopen("modules.conf", "r");
    if (!fp)
    {
        perror("fopen");
        return NULL;
    }
    
    size_t 
    char **lines = calloc(
    
    size_t buf_size = 100;
    char[] buf = char[buf_size];
    size_t bytes;
    while ((bytes = fread(buf, sizeof(char), buf_size, fp)))
    {
        
    }
}

int main(int argc, char *argv[])
{
    
    
}
