from pathlib import Path


if not Path("vectorstore").exists():
    from rag.ingest import main
    main()