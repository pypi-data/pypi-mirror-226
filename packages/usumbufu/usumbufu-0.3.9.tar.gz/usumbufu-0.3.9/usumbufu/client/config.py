def apply_args(config, args, extra_args={}):
    for k in extra_args.keys():
        v = extra_args[k]
        if v == None:
            v = '_' + k.upper()
        r =  getattr(args, k)
        existing_r = None
        try:
            existing_r = config.get(v)
        except KeyError:
            pass
        if existing_r == None or r != None:
            config.add(r, v, exists_ok=True)
