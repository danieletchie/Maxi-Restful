def add_parser_args(parser, args_name, args_type,default=None, args_required=False, args_help=None):
        parser.add_argument(
            args_name,
            type=args_type,
            default=default,
            required=args_required,
            help=args_help
        )
