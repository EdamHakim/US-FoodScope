"""
Management command to initialize the RAG pipeline.

Usage:
    python manage.py init_rag [--force]

This command:
1. Downloads rag_df.csv from Hugging Face Hub
2. Transforms data to text
3. Chunks the text
4. Generates embeddings
5. Builds FAISS index
6. Caches everything for fast startup
"""

from django.core.management.base import BaseCommand
from rag.services import get_rag_service
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Initialize the RAG pipeline by building the vector index'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force rebuild even if index exists',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Initializing RAG pipeline...'))
        
        force_rebuild = options.get('force', False)
        
        try:
            rag_service = get_rag_service()
            rag_service.initialize(force_rebuild=force_rebuild)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ RAG pipeline initialized successfully!\n'
                    f'  Index contains {rag_service.vector_storage.index.ntotal} vectors\n'
                    f'  Ready to answer questions about U.S. food environment data.'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Error initializing RAG pipeline: {str(e)}')
            )
            raise

